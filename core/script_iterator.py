import os
from datetime import datetime
import logging
import random
import subprocess
import time
import traceback
from datetime import datetime

from adbutils.errors import AdbError
import requests
import sentry_sdk
import uiautomator2 as u2

import config
from core.activity import AppActivity
from core.activity_scanner import ActivityScanner
import core.exceptions
from core.thread import ThreadWithTrace
from iterator_models import DeviceInfo, Account, Campaign, Options, Messages, IteratorAnswer, Proxy
from scrip_iterations_rules import phone_preparation
from services import telephony, utils
from services.db import get_warm_status, get_phones_warm
from services.photos.photos_manager import remove_all_photos
from services.props import contacts


sentry_sdk.init(dsn="https://a32fb9b2252544609dbe4f6d882825f4@sentry.caltat.com/5")


class ScriptIterator:

    def __init__(self, wa_version, task, device_info: DeviceInfo, account: Account, campaign: Campaign, messages: Messages, options: Options, proxy: Proxy = None, cdn=config.CDN):
        self.logger = None

        """ Params """
        self.app = account.app
        self.task = task
        self.serial = device_info.serial
        self.device_info = device_info
        self.account = account
        self.campaign = campaign
        self.messages = messages
        self.options = options
        self.cdn = cdn
        self.wa_version = wa_version
        self.is_process_active = True

        """ Рассылка в группы / коммьюнити """
        group_sending = campaign.parameters.get('group_sending')
        self.group_sending = group_sending.get('enabled')
        self.group_community_sending = group_sending.get('community_sending')
        self.group_message = group_sending.get('message')
        self.group_sending_with_image = group_sending.get('sending_with_image')
        self.group_with_image = group_sending.get('group_with_image')
        self.community_with_image = group_sending.get('community_with_image')
        images = group_sending.get('images')
        self.community_image = None
        self.group_image = None
        self.sending_image = None

        # Скачиваем изображения на локалку, если идет рассылка, чтобы не тратить ресурсы
        if self.task == 'send':
            if self.group_with_image:
                self.group_image = random.choice(images)
                self.group_image = utils.GroupImage.download(self.group_image, self.serial)

            if self.community_with_image:
                self.community_image = random.choice(images)
                self.community_image = utils.GroupImage.download(self.community_image, self.serial)

            if self.group_sending_with_image:
                self.sending_image = random.choice(images)
                self.sending_image = utils.GroupImage.download(self.sending_image, self.serial)

        self.group_name = random.choice(group_sending.get('group_name'))
        self.group_name_original = self.group_name
        self.community_name = group_sending.get('community_name')
        self.community_pattern = group_sending.get('community_pattern')
        self.group_pattern = group_sending.get('group_pattern')

        # Генерация случайного названия коммьюнити и групп
        utils.generate_name_by_pattern(self)

        # Рассылка по нескольким группам
        self.chunks_enabled = group_sending.get('chunks_enabled')
        if self.chunks_enabled:
            self.group_messages_per_chunk = group_sending.get('messages_per_chunk')
            # [(message, uniq_id), ...]
            self.group_chunked_messages = [(item, item[0]['message'].split('/')[-1]) for item in list(
                utils.divide_chunks(sorted(self.messages.messages_to_send, key=lambda x: x['phone']),
                                    self.group_messages_per_chunk))]
            self.group_message_sent = {}

        self.group_set_name = False
        self.group_community_set_name = False
        self.group_participants_inserted = None
        self.group_permission_set = None
        self.group_community_set_photo = None
        self.group_set_photo = None
        self.group_created = False
        self.strange_community = None  # чужое комьюнити
        self.invalid_photo = None  # разрешение херовое
        self.conversation_exists = 0  # в будущем заменить эту херню

        """ Default """
        self.d = None
        self.current_activity = None
        self.thread = None
        self.wa_ready = False
        self.stop = False
        self.stop_hard = False
        self.finished = False
        self.last_sent = None

        """ Account """
        self.client = None
        self.change_name = False
        self.change_photo = False
        # hardcode
        self.account.two_step_auth_code = campaign.parameters['two_step_auth_code'] if not account.two_step_auth_code else account.two_step_auth_code
        self.account.photo = campaign.parameters['photo'] if not account.photo else account.photo
        self.account.about = campaign.parameters['about'] if not account.about else account.about
        if options.data_for_account:
            if task == 'reg':
                account.linked_info = options.data_for_account.id
            elif not account.linked_info:
                self.change_name = True
                self.change_photo = False
            elif not account.photo:
                self.change_photo = False

        """ Reg service """
        self.code_requested = False
        self.code_requested_counter = 0
        self.request_again = False
        self.phone_code = None
        self.phone_num = None
        self.reg_phones_entry_limit = campaign.parameters['reg_phones_entry_limit']
        self.all_countries = None
        self.tmp_reg_aggregators = None
        self.current_activator = None
        self.country = None
        self.start_reg_timestamp = None
        self.finish_reg_timestamp = None
        self.country_tries = campaign.parameters['country_tries']
        self.options.timeout_getting_code = campaign.parameters['timeout_getting_code']

        """ Backups """
        self.restore_backup = True
        self.backup_service = None
        self.failed_web = False

        """ Contacts """
        self.contacts_refresh_attempts = 0
        self.contacts_refreshed = False

        """ Calls """
        self.calls_enabled = self.campaign.parameters['calling']['enabled']
        self.calls_finished = None
        self.first_calls_enabled = self.campaign.parameters['calling']['enabled']
        self.had_incoming_call = None
        if self.task == 'send' and self.calls_enabled:
            self.calls_enabled = get_warm_status(self.campaign.id, self.account.id)

        if self.calls_enabled:
            self.call_times = self.campaign.parameters['calling']['call_times']
            self.talking_timeout_seconds = self.campaign.parameters['calling']['talking_timeout_seconds']
            self.to_call_timeout_seconds = self.campaign.parameters['calling']['to_call_timeout_seconds']
            self.all_call_phones = self.campaign.parameters['bots_phones']
            self.call_phones = random.sample(self.all_call_phones, len(self.all_call_phones))[:self.call_times]
            self.device_info.params['phones_to_call'] = self.call_phones
        else:
            self.call_times = None
            self.talking_timeout_seconds = None
            self.to_call_timeout_seconds = None
            self.all_call_phones = None
            self.call_phones = None

        """ Images """
        self.just_sent_image = False
        self.image_loaded = False

        """ For refactor """
        self.tmp_category = False

        """ Current campaign settings"""
        self.device_info.params['campaign_settings'] = {key: value for key, value in self.campaign.__dict__.items() if key not in config.DUPLICATE_PARAMETERS}

        """ Technical settings """
        self.max_cnt_calls = campaign.parameters['max_cnt_calls']
        self.min_cnt_calls = campaign.parameters['min_cnt_calls']
        self.is_night_mode = self.campaign.parameters['night_mode']

        """ Bots """
        self.bots_enable = self.campaign.parameters['bots_enable']
        self.bots_finished = None
        self.first_bots_enable = self.campaign.parameters['bots_enable']
        self.without_internet_w_warm = self.campaign.parameters['without_internet_w_warm']
        if self.task == 'send' and not self.first_calls_enabled:
            self.bots_enable = get_warm_status(self.campaign.id, self.account.id)
        if self.bots_enable:
            self.bots_phones = self.campaign.parameters['bots_phones']
            self.bots_messages = self.campaign.parameters['bots_messages']
            self.bots_amount = self.campaign.parameters['bots_amount']
            # bots_current_phones имеют структуру как messages_to_send только для ботов
            self.bots_current_phones = get_phones_warm(self.campaign.id).get('messages')
            self.bots_pause_enable = self.campaign.parameters['bots_pause_enable']
            self.bots_breaktime_min = self.campaign.parameters['bots_breaktime_min']
            self.bots_breaktime_rand = self.campaign.parameters['bots_breaktime_rand']
        else:
            self.bots_phones = None
            self.bots_messages = None
            self.bots_amount = None
            # чтобы заливать не все номера ботов, а сколько надо
            self.bots_current_phones = None
            self.bots_pause_enable = None
            self.bots_breaktime_min = None
            self.bots_breaktime_rand = None

        """ Proxy """  # type 1: HTTPS, 2: SOCKS4a, 3: SOCKS5
        self.proxy = proxy
        if proxy:
            self.proxy_ready = False
            self.options.code_activator.region = proxy.country

        """Code Activator Stat"""
        self.activators_with_responses = ('drop_sms_getsms', 'sms_activate')
        self.drop_sms_response_enable = campaign.parameters.get('drop_sms_response_enable')
        self.device_info.params['drop_sms_response'] = []
        self.sms_activate_response_enable = campaign.parameters.get('sms_activate_response_enable')
        self.device_info.params['sms_activate_response'] = {'responses': [], 'prices': []}

        """Timeout Checker"""
        self.start_time = None

    # def __getattr__(self, item):
    #     """ Если обращаемся к аттрибуту, которого нету, то вместо ошибки ловим false """
    #     return False

    @property
    def current_activity(self) -> AppActivity:
        return self._current_activity

    @current_activity.setter
    def current_activity(self, activity: AppActivity):
        self._current_activity = activity

    def do_next_iter(self):
        try:
            """ Обработка окон """
            if activity_method := self.options.activities_methods.get(self.current_activity):
                activity_method(self)
            else:
                # Скриншот экрана при возникновении необработанной активности
                screenshot_name = f'{self.current_activity.activity_name[1:]}_{self.serial}_{str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))}.jpg'
                self.d.screenshot().save(f'{os.getcwd()}/screenshots/{screenshot_name}')
                self.device_info.params['unknown_activities'] = {'screenshot': screenshot_name, 'activity': self.current_activity.activity_name}
                self.logger.error(f'unknown activity!\n{self.current_activity}')

                with open(f'{os.getcwd()}/screenshots/{screenshot_name}', 'rb') as file:
                    self.send_telegram_error(file)

                self.stop = True
                self.stop_hard = True
        except core.exceptions.BanException:
            self.logger.warning(f'ban!')

            self.check_messages()

            self.stop = True
            self.stop_hard = True
            self.finished = True
        except core.exceptions.StopThreadException:
            if self.task == 'send' and self.messages.messages_sent:
                #  ждем пока отправятся последние сообщения
                time.sleep(1)
                self.check_messages()
                if self.campaign.read_messages:
                    phone_preparation.turn_airplane_mode(self.d, on=True)
                    utils.get_wa_answers(self.d)
                    utils.delete_wa_answers(self.d)
            self.stop = True
            self.finished = True
        except AdbError:
            ...
        except RuntimeError:
            ...

    def send_telegram_error(self, file):
        """ В случае неизвестной активности шлем скриншот в телеграм канал (AlarmBot) """

        files = {
            'project_name': (None, 'WHATSAPP'),
            'message': (None, f'[{config.DB_MODE.upper()}]📱Device: {self.serial}; ❓Unknown activity: {self.current_activity}'),
            'file': (file.name, file, 'image/jpeg'),
        }

        try:
            response = requests.post('http://65.108.49.8:6100/error', files=files,
                                     headers={"accept": "application/json", 'Token': '24ca36a3fed4f79a1c7e17b74c4343da'},
                                     timeout=60)
        except Exception as e:
            if isinstance(e, requests.exceptions.ReadTimeout):
                self.logger.error('Ошибка таймаута при отсылке смс в бота(АЛАРМ)')
            else:
                self.logger.error(f'Ошибка неизвестная при отсылке смс в бота(АЛАРМ): {e}')
        else:
            self.logger.info(f'Sent error to telegram channel with {response.status_code}')

    def check_activity(self):
        """ Пока обрабатывается окно, проверяет не изменилась ли активность """

        deadline = None
        global_deadline = time.time() + 360
        while self.stop is False:
            new_activity = ActivityScanner(self.d).scan()
            if new_activity != self.current_activity:
                self.current_activity = new_activity

                if self.thread.is_alive():
                    self.thread.kill()
                break

            if not self.thread.is_alive() and not deadline:
                t = self.options.timeout_new_iter_loading if self.current_activity.is_loading else self.options.timeout_new_iter
                if "call" in self.current_activity.activity_name:
                    t = self.options.timeout_new_iter_loading
                deadline = time.time() + t
            if deadline and time.time() >= deadline:
                self.logger.error(f'timeout new activity! last activity - {self.current_activity}')
                if self.task == 'send' and self.messages.messages_sent:
                    self.check_messages()
                    if self.campaign.read_messages:
                        phone_preparation.turn_airplane_mode(self.d, on=True)
                        utils.get_wa_answers(self.d)
                        utils.delete_wa_answers(self.d)
                self.stop = True
                self.stop_hard = True
                break

            # стоп итерации если зависли
            if time.time() >= global_deadline:
                self.logger.error(f'timeout global deadline! last activity - {self.current_activity}')
                if self.task == 'send' and self.messages.messages_sent:
                    self.check_messages()
                    if self.campaign.read_messages:
                        phone_preparation.turn_airplane_mode(self.d, on=True)
                        utils.get_wa_answers(self.d)
                        utils.delete_wa_answers(self.d)
                self.stop = True
                self.stop_hard = True
                break

    def start_preparing(self):
        self.logger.info('start connect u2')
        time.sleep(0.2)
        self.logger.info('start connect u2 1')
        time.sleep(0.2)
        self.logger.info('start connect u2 2')
        time.sleep(0.2)
        self.logger.info('start connect u2 3')
        time.sleep(0.2)
        self.logger.info('start connect u2 4')
        self.d = u2.connect(self.serial)
        self.logger.info('end connect u2')
        self.d.reset_uiautomator()
        self.logger.info('end reset_uiautomator')
        self.d.screen_on()
        self.logger.info('end screen_on')
        self.d.keyevent('home')
        if self.task == 'reg':
            self.logger.info('start set_time')
            self.set_time(self.is_night_mode)
            self.logger.info('end set_time')
        self.logger.info('start get_display')
        display = utils.get_display(self.d)
        self.logger.info('end get_display')
        if display.get('text', 'Not now').exists:
            self.d(text='Not now').click()
        if display.get('text', 'Check for update').exists:
            self.d(text='Check for update').click()
            self.d.keyevent('home')
        if self.campaign.without_internet:
            self.device_info.params['without_internet'] = True
        if self.proxy:
            self.device_info.params['proxy_enable'] = True

        self.logger.info('start app_stop')
        self.d.app_stop(self.app)
        self.logger.info('end app_stop')
        # Отключение инета перед вставкой контактов (возможно из-за этого ошибка при синхронизации)
        phone_preparation.turn_airplane_mode(self.d, on=True)
        self.logger.info('end turn_airplane_mode')
        self.d.shell("content delete --uri content://com.android.contacts/data/ --where \"is_sim=1\"")
        self.logger.info('end shell delete')
        sim_contacts = self.d.shell("content query --uri content://icc/adn/").output
        self.logger.info('end shell content')
        for contact in sim_contacts.split('\n'):
            if 'adn_index=' in contact:
                adn_index = contact.split('adn_index=')[1].split(',')[0]
                self.d.shell(f'content delete --uri content://icc/adn/ --where "adn_index={adn_index}"')
        self.logger.info('end for sim_contacts')

        if self.options.contacts.phones:
            contacts_list = [{'phone': phone} for phone in self.options.contacts.phones]

            # рассылка с ботами
            if self.bots_enable:
                contacts_list += [{'phone': phone['phone']} for phone in self.bots_current_phones]
                self.logger.info('bots contacts inserted')

            # Случайные контакты для исключения пересечений
            for i in range(max(80 - len(contacts_list), self.campaign.contacts_send)):
                contacts_list.append({'phone': str(random.randint(79000000000, 79999999999))})

            if self.calls_enabled:
                contacts_list += [{'phone': phone} for phone in self.call_phones]
                self.logger.info(f'calls contacts inserted')
                # self.logger.info(f'Номера для звонков: {self.call_phones}')
                # self.logger.info(f'Все номера: {contacts_list}')
            self.logger.info('start add_from_list')
            contacts.add_from_list(self.d, contacts_list)
            self.logger.info('end add_from_list')

        # elif self.options.just_connected:
        else:
            self.logger.info('start randomize ')
            contacts.randomize(self.d, self.campaign.contacts_reg)
            self.logger.info('end randomize')

        # рандомизация даты добавления контактов
        if self.campaign.parameters['randomize_contacts_date']:
            time.sleep(5)  # контакты некоторое время подгружаются еще в базу
            amount_contacts = utils.randomize_samsung_contacts(self.d)
            self.logger.info(f"randomized {amount_contacts} contacts")

        if not self.campaign.parameters['reload_backup']:
            files = self.d.shell(f'ls {config.PHONE_TMP_FOLDER}').output.split('\n')
            for file in files:
                if file[:7] == 'backup_':
                    if self.account.backup and file[7:] == self.account.backup:
                        self.restore_backup = False
                    else:
                        self.d.shell(f'rm {config.PHONE_TMP_FOLDER}/{file}')

        if self.restore_backup:
            self.d.app_stop(self.app)
            self.d.shell(f"pm clear {self.app}")

        phone_preparation.turn_airplane_mode(self.d, on=False)
        phone_preparation.turn_off_wifi(self.d)
        phone_preparation.turn_internet(self.d, on=True)
        phone_preparation.turn_off_accelerometer_rotation(self.d)
        phone_preparation.set_screen_timeout(self.d)
        phone_preparation.disable_lockscreen_swipe(self.d)
        if self.proxy:
            if self.proxy.change or utils.is_now_in_interval(0, 1):
                self.d.shell("pm uninstall org.sandroproxy.drony")
                ip = phone_preparation.check_internet(self.d)
            ip = self.proxy.country
        else:
            self.d.shell("pm uninstall org.sandroproxy.drony")
            ip = phone_preparation.check_internet(self.d)
        self.device_info.ip = ip
        if subprocess.call(f'adb -s {self.serial} shell "su -c /data/local/sqlite3 --version"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            subprocess.run([f"adb -s {self.serial} push services/sqlite3 /data/local/tmp"], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.call(f'adb -s {self.serial} shell  "su -c mv /data/local/tmp/sqlite3 /data/local/; su -c chmod 775 /data/local/sqlite3"', shell=True, stdout=subprocess.DEVNULL)

        if self.proxy:
            self.install_drony()
            if self.proxy.link:
                if not utils.change_proxy_ip(self.proxy.link):
                    self.logger.warning(f'cant change proxy ip for {self.proxy.host}')

            if self.task == 'reg':
                self.options.reg_aggregators = list(filter(lambda s: s.country == self.proxy.country, self.options.reg_aggregators))
                if len(self.options.reg_aggregators) == 0:
                    self.logger.error(f'no reg_aggregators for this proxy {self.proxy.country}')
                    raise core.exceptions.StopThreadException
            self.proxy_ready = utils.check_proxy(self.d, self.proxy.host, self.proxy.port, self.proxy.username, self.proxy.password, self.proxy.type)

        # чтобы на итерацию была только одна страна
        if self.campaign.one_country_iter:
            countries = list({r.country for r in self.options.reg_aggregators})
            self.all_countries = random.sample(countries, len(countries))

        if self.restore_backup:
            remove_all_photos(self.d)
            telephony.clear_calls(self.d)
            param_cnt_calls = random.randint(self.min_cnt_calls, self.max_cnt_calls)

            if self.calls_enabled:
                for phone in self.options.contacts.phones[:param_cnt_calls]:
                    telephony.add_random_call(self.d, tel_phone=phone)
            else:
                for i in range(param_cnt_calls):
                    telephony.add_random_call(self.d)

            self.device_info.params['calls_added'] = param_cnt_calls

            param_battery_status = random.randint(2, 3)
            param_battery_level = random.randint(1, 100)
            self.d.shell(f'dumpsys battery set status {param_battery_status}')
            self.d.shell(f'dumpsys battery set level {param_battery_level}')
            self.d.shell(f'dumpsys battery set usb 0')
            if param_battery_status == 2:
                self.d.shell(f'dumpsys battery set ac 1')
            else:
                self.d.shell(f'dumpsys battery set ac 0')
            self.device_info.params['charging'] = True if param_battery_status == 2 else False
            self.device_info.params['battery_level'] = param_battery_level

            param_night_mode = random.choice(["yes", "no"])
            param_brightness = random.randint(60, 200)
            self.d.shell(f'cmd uimode night {param_night_mode}')
            self.d.shell(f'settings put system screen_brightness {param_brightness}')
            self.device_info.params['night_mode'] = True if param_night_mode == 'yes' else False
            self.device_info.params['brightness'] = param_brightness

            # Для крепкого сна
            if 9 <= datetime.now().hour < 22:
                self.d.shell(f'cmd notification set_dnd off')
                for i in (1, 2, 3, 4, 5, 6):
                    param_volume = random.randint(0, 15)
                    self.d.shell(f'cmd media_session volume --stream {i} --set {param_volume}')
                    self.device_info.params[f'volume_{i}'] = param_volume

        self.d.shell(f'cmd notification set_dnd priority')

        if self.serial not in config.DEVICE_125:
            param_file_size = random.randint(0, 6000)
        else:
            param_file_size = random.randint(0, 200)
        self.d.shell(f'rm {config.PHONE_TMP_FOLDER}/clear_file')
        self.d.shell(f'fallocate -l {param_file_size}M {config.PHONE_TMP_FOLDER}/clear_file"')
        self.device_info.params['file_size'] = param_file_size
        if self.task != 'reg':
            self.d.set_fastinput_ime(False)
            self.d.shell(f'ime set com.samsung.android.honeyboard/.service.HoneyBoardService')
        else:
            self.d.set_fastinput_ime(True)

    def finish(self, working_devices: dict):
        self.d.keyevent('home')
        if self.stop_hard:
            self.d.app_stop(self.app)
        phone_preparation.turn_airplane_mode(self.d, on=True)
        self.d.screen_off()
        if self.account.code:
            self.logger.info(f'REG CODE: {self.account.code} by {self.options.code_activator.NAME}')
        self.is_process_active = False
        self.logger.info(f'set is_process_active {self.is_process_active}')
        working_devices[self.serial] = IteratorAnswer(task=self.task, device_info=self.device_info, account=self.account, campaign=self.campaign, messages=self.messages, options=self.options, start_time=self.start_time, is_process_active=self.is_process_active)
        self.logger.info(f'update  working_devices in finish ()')



    def run(self, working_devices):
        self.config = self.customize_config()
        self.start_time = datetime.now()
        try:
            working_devices[self.serial] = IteratorAnswer(task=self.task, device_info=self.device_info, account=self.account, campaign=self.campaign, messages=self.messages, options=self.options, start_time=self.start_time, is_process_active=self.is_process_active)
            config.prepare_logging()
            # Создание обработчика для записи в файл
            file_handler = logging.FileHandler('./whatsapp.log')

            # Настройка формата логов для файла (если необходимо)
            file_formatter = logging.Formatter('[%(asctime)s] %(name)s: [%(levelname)s] %(message)s', datefmt='%d %b %H:%M:%S')
            file_handler.setFormatter(file_formatter)

            self.logger = logging.getLogger(self.serial)
            self.logger.addHandler(file_handler)
            self.logger.info('preparing device...')
            self.logger.info('do nothing 5 seconds')
            for x in range(5):
                self.logger.info(f'do nothing {x}')
                time.sleep(1)
            self.start_preparing()
            self.current_activity = ActivityScanner(self.d).scan()

            while True:
                self.logger.info(self.current_activity)
                self.thread = ThreadWithTrace(target=self.do_next_iter)
                self.thread.start()
                self.check_activity()
                working_devices[self.serial] = IteratorAnswer(task=self.task, device_info=self.device_info, account=self.account, campaign=self.campaign, messages=self.messages, options=self.options, start_time=self.start_time, is_process_active=self.is_process_active)
                if self.stop:
                    self.finish(working_devices)
                    working_devices[self.serial] = IteratorAnswer(task=self.task, device_info=self.device_info, account=self.account, campaign=self.campaign, messages=self.messages, options=self.options, start_time=self.start_time, is_process_active=self.is_process_active)
                    self.logger.info('After finish()')
                    break

        except BaseException as e:

            working_devices[self.serial] = IteratorAnswer(task=self.task, device_info=self.device_info, account=self.account, campaign=self.campaign, messages=self.messages, options=self.options, start_time=self.start_time, is_process_active=self.is_process_active)
            self.handle_exception(e, working_devices)
        finally:
            self.is_process_active = False
            working_devices[self.serial] = IteratorAnswer(task=self.task, device_info=self.device_info, account=self.account, campaign=self.campaign, messages=self.messages, options=self.options, start_time=self.start_time, is_process_active=self.is_process_active)

    def check_messages(self):
        # Восстановление не отправленных сообщений по логу WhatsApp
        if self.messages.messages_sent:
            sent, not_sent = [], []
            group_links_sent = []
            if self.group_sending and self.chunks_enabled:
                # Если чанки, то ищем uniq_id в отосланных сообщениях в базе ватсапа {uniq_id: messages, ...}
                sent_message_texts = utils.get_wa_group_messages(self.d)
                for uniq_id in self.group_message_sent.keys():
                    if uniq_id in sent_message_texts:
                        sent.extend(self.group_message_sent[uniq_id])
                        group_links_sent.append(uniq_id)
                    else:
                        not_sent.extend(self.group_message_sent[uniq_id])
                self.device_info.params['group_links_sent'] = group_links_sent

            else:
                messages_log = utils.get_wa_messages(self.d, self.account.banned)
                status_message = utils.get_wa_phone_status(self.d)
                self.device_info.params['message_status'] = status_message
                for message in self.messages.messages_sent:
                    try:
                        status = messages_log[message['phone']]
                        not_sent.append(message) if status == 'not sent' else sent.append(message)

                    except KeyError:
                        if self.calls_enabled and message['message'] in ('declined', 'no_answer', 'accepted'):
                            sent.append(message)
                        if self.group_sending:
                            sent.append(message)
                        self.logger.warning(f"{message['phone']} not in messages_log")

            self.messages.messages_sent = sent
            self.messages.messages_to_send += not_sent

    def customize_config(self):
        # рег агрегаторы с привязкой к компании
        if self.campaign.reg_aggregators:
            self.options.reg_aggregators = self.campaign.reg_aggregators
            self.campaign.reg_aggregators = None

    def set_time(self, is_night_mode):
        if is_night_mode:
            date = datetime.now()
            if int(self.d.shell('date +%H').output) > 2:
                self.d.shell("""settings put global auto_time 0""")
                self.d.shell("""su -c 'date {:02}{:02}00{:02}{:02}.{:02};am broadcast -a android.intent.action.TIME_SET'""".format(date.month, date.day, date.minute, date.year, date.second))
        else:
            self.d.shell("""settings put global auto_time 1""")

    def install_drony(self):
        out = self.d.shell(f"pm list packages | grep org.sandroproxy.drony").output
        if 'package:org.sandroproxy.drony' not in out:
            for x in range(5):
                try:
                    answer = subprocess.run(f"adb -s {self.serial} install -d apk/drony.apk", shell=True, capture_output=True, timeout=120, text=True).stdout
                except subprocess.TimeoutExpired as e:
                    if self.d.shell(f'pm list packages | grep org.sandroproxy.drony').output == '':
                        self.logger.warning('cant install drony, retry')
                        continue
                    else:
                        self.logger.info(f'drony installed but error occurred: {e}')
                        break
                break
            # subprocess.run(f"adb -s {self.serial} install -d apk/drony.apk", shell=True, stdout=subprocess.DEVNULL, timeout=120)
            self.d.shell(f"pm grant org.sandroproxy.drony android.permission.ACCESS_COARSE_LOCATION")
            self.d.shell(f"pm grant org.sandroproxy.drony android.permission.ACCESS_BACKGROUND_LOCATION")
            self.d.shell(f"pm grant org.sandroproxy.drony android.permission.READ_EXTERNAL_STORAGE")
            self.d.shell(f"pm grant org.sandroproxy.drony android.permission.WRITE_EXTERNAL_STORAGE")

    def handle_exception(self, e, working_devices):
        call_finish = False

        if isinstance(e, AdbError) or isinstance(e, RuntimeError):
            self.logger.error(f'device disconnected!')
            call_finish = True

        elif (isinstance(e, EnvironmentError) and 'Errno Uiautomator started failed.' in str(e)) or isinstance(e, requests.exceptions.ReadTimeout):
            self.logger.error(f"device doesn't work, reboot...")
            self.d.reset_uiautomator()
            time.sleep(10)

        elif isinstance(e, core.exceptions.NoInternetException):
            self.logger.error(f'no internet!')
            call_finish = True

        elif isinstance(e, core.exceptions.NoWhatsappException):
            self.logger.error(f'whatsapp not installed!')
            call_finish = True

        elif isinstance(e, contacts.ContactsUpdateException):
            self.logger.error(f'cant update contacts, reboot...')
            subprocess.call(f"adb -s {self.serial} reboot", shell=True, stdout=subprocess.DEVNULL)
            time.sleep(5)
            call_finish = True


        elif isinstance(e, KeyboardInterrupt):
            self.logger.error(f'keyboard interrupt!')
            call_finish = True
            self.stop_hard = True

        else:
            self.logger.error(f'unknown exception! {e}')
            traceback.print_exc()
            call_finish = True
            self.stop_hard = True

        if call_finish:
            try:
                self.finish(working_devices)
                self.logger.info('After finish in call_finish')
            except:
                ...
