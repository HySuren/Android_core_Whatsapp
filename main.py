import os

import psutil
import sentry_sdk
import multiprocessing
import traceback
import time
import logging
from iterator_models import DeviceInfo, Account, Options, Messages, Config, Contacts
from services import db
from services import utils
from core.script_iterator import ScriptIterator
from scrip_iterations_rules.rules import ACTIVITY__METHODS_DICT
import subprocess
import config
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from services.cdn.selectel import SelectelCDN
from core.list import ThreadSafeList

sentry_sdk.init(dsn="https://a32fb9b2252544609dbe4f6d882825f4@sentry.caltat.com/5")


class Main:
    def __init__(self):
        config.prepare_logging()
        # Создание обработчика для записи в файл
        file_handler = logging.FileHandler('./whatsapp.log')

        # Настройка формата логов для файла (если необходимо)
        file_formatter = logging.Formatter('[%(asctime)s] %(name)s: [%(levelname)s] %(message)s', datefmt='%d %b %H:%M:%S')
        file_handler.setFormatter(file_formatter)
        self.logger = logging.getLogger('MAIN')
        self.logger.addHandler(file_handler)

        manager = multiprocessing.Manager()
        self.working_accounts_data = manager.dict()
        self.working_accounts_processes = ThreadSafeList()
        self.mac = utils.get_mac()
        self.CONFIG = Config()
        self.devices = []
        self.new_connected_devices = []
        self.stopped = False
        self.checker_started = False
        self.checker_working_accounts_started = False
        self.checker_timeout_process = False
        self.MAX_THREADS = 15
        self.last_processes_info_created = datetime.min

        self.print_startup_info()

    def print_startup_info(self):
        self.logger.info(f'farm: {self.mac}')

    def get_db_config(self):
        was_enabled = self.CONFIG.enable_new_iters
        self.CONFIG = db.get_config()
        if not was_enabled and self.CONFIG.enable_new_iters:
            self.logger.info(f'new iterations enabled!')
        if was_enabled and not self.CONFIG.enable_new_iters:
            self.logger.info(f'new iterations disabled!')

    def get_bool_from_config(self, field):
        return self.CONFIG.proxy_status[self.mac][field] if self.CONFIG.proxy_status.get(self.mac, {}).get(field) in (True, False) else self.CONFIG.proxy_status['default'][field]

    def check_devices(self):
        active_devices, bad_devices = utils.get_list_adb(bad_devices_125=self.CONFIG.bad_devices)
        for serial in list(filter(lambda s: s not in self.devices, active_devices)):
            self.logger.info(f'device {serial} connected!')
            db.update_device(serial=serial, farm=self.mac)
            self.new_connected_devices.append(serial)
            self.devices.append(serial)
        for serial in list(filter(lambda s: s not in active_devices, self.devices)):
            self.logger.info(f'device {serial} disconnected!')
            db.update_device(serial=serial, farm=None)
            self.devices.remove(serial)

    def check_can_be_stop(self):
        if not self.working_accounts_data and not self.CONFIG.enable_new_iters:
            self.logger.info(f'all iterations finished, service can be stopped...')
            time.sleep(5)

    def launch_sending(self, serial, account, proxy=None):
        # Тесты по разным кампаниям
        is_sending_test = False
        if self.CONFIG.campaign_test:
            is_sending_test = self.CONFIG.campaign_test.get(self.mac).get('send') if self.CONFIG.campaign_test.get(self.mac) else self.CONFIG.campaign_test.get('default').get('send')

        if is_sending_test:
            campaign = db.get_campaign_by_serial(serial=serial)
        else:
            campaign = db.get_campaign_by_account(account=account)

        limit = self.CONFIG.messages_limit if campaign.messages_limit is None else campaign.messages_limit
        messages = db.get_messages(campaign=campaign, limit=limit, domain=self.CONFIG.links_domain, account=account)
        contacts = Contacts(phones=[i['phone'] for i in messages.messages_to_send])
        db.set_account_in_work(account=account, in_work=True)
        if account.linked_info:
            data_for_account = db.get_generated_account_info(account.linked_info)
        else:
            data_for_account = db.generate_random_account_info()

        self.logger.info(f'device {serial} (ACCOUNT#{account.id}) launching: sending {len(messages.messages_to_send)} messages with {campaign.messages_breaktime_min}-{campaign.messages_breaktime_min + campaign.messages_breaktime_rand}s timeout' + (f' and {proxy.country} proxy' if proxy else ''))
        self.launch_session(task='send', serial=serial, campaign=campaign, account=account, messages=messages, contacts=contacts, data_for_account=data_for_account, proxy=proxy)

    def launch_registration(self, serial, campaign, proxy=None):
        self.logger.info(f'device {serial}: registering account for CAMPAIGN#{campaign.id}' + (f' and {proxy.country} proxy' if proxy else ''))
        data_for_account = db.generate_random_account_info()
        self.launch_session(task='reg', serial=serial, campaign=campaign, account=Account(app=self.CONFIG.app), messages=Messages(), contacts=Contacts(), data_for_account=data_for_account, proxy=proxy)

    def launch_web_scan(self, serial, account, proxy=None):
        campaign = db.get_campaign_by_account(account=account)
        db.set_account_in_work(account=account, in_work=True)
        contacts = db.get_contacts(account.id, campaign.id)
        if contacts.phones:
            if account.linked_info:
                data_for_account = db.get_generated_account_info(account.linked_info)
            else:
                data_for_account = db.generate_random_account_info()

            self.logger.info(f'device {serial} (ACCOUNT#{account.id}) launching: scan WEB' + (f' and {proxy.country} proxy' if proxy else ''))
            self.launch_session(task='scan', serial=serial, campaign=campaign, account=account, messages=Messages(), contacts=contacts, data_for_account=data_for_account, proxy=proxy)
        else:
            db.set_account_in_work(account=account, in_work=False)

    def launch_session(self, task, serial, campaign, account, messages, contacts, proxy=None, data_for_account=None):
        if serial in self.new_connected_devices:
            just_connected = True
            self.new_connected_devices.remove(serial)
        else:
            just_connected = False
        make_web_backup = True if config.ENABLE_WEB_BACKUP and task == 'scan' else False
        utils.set_default_params(parent=self.CONFIG, child=campaign)
        options = Options(activities_methods=ACTIVITY__METHODS_DICT, reg_aggregators=self.CONFIG.reg_aggregators,
                          reinstall_wa=self.CONFIG.reinstall_wa, retry_bad_phone=self.CONFIG.reg_bad_phones_retries,
                          read_messages=campaign.read_messages, messages_breaktime_min=campaign.messages_breaktime_min,
                          messages_breaktime_rand=campaign.messages_breaktime_rand, make_web_backup=make_web_backup,
                          just_connected=just_connected, data_for_account=data_for_account, contacts=contacts)
        try:
            worker = ScriptIterator(task=task, device_info=DeviceInfo(serial=serial), account=account,
                                    campaign=campaign, options=options, messages=messages, cdn=config.CDN, proxy=proxy,
                                    wa_version=self.CONFIG.wa_version)
            p = multiprocessing.Process(target=worker.run, args=(self.working_accounts_data,), daemon=True, name=serial)
            p.start()
            self.logger.info(f'{serial}: After script iterator')
            self.working_accounts_data[serial] = None
            self.working_accounts_processes.append(p)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            self.logger.error(f'{serial}: ScriptIterator issue in main: {e}')

    def processes_info(self, active_processes: list[str], finished_processes: dict, finished_processes_multithread_list: list[list]) -> None:
        self.logger.info("[DEBUG] active_processes: " + str(active_processes))
        # self.logger.info("[DEBUG] active_processes_len: " + str(active_processes))
        self.logger.info("[DEBUG] finished_processes: " + str(finished_processes))
        # self.logger.info("[DEBUG] finished_processes_len: " + str(len(finished_processes)))
        # self.logger.info("[DEBUG] finished_processes_multithr_list: " + str(len(finished_processes_multithread_list)))

    def check_working_accounts(self):
        active_processes = []
        for k, v in self.working_accounts_data.items():
            if v and v.is_process_active:
                active_processes.append(k)
        # self.logger.info(f'active_processes: {active_processes}')
        finished_processes = {}
        finished_processes_keys_list = []

        for k, v in self.working_accounts_data.items():
            if v and not v.is_process_active:
                finished_processes[k] = v
                finished_processes_keys_list.append(k)
        # self.logger.info(f'finished_processes: { finished_processes.keys()}')

        finished_processes_multithread_list = [[k, v] for k, v in finished_processes.items()]

        if self.last_processes_info_created >= datetime.now() - timedelta(seconds=5):
            time.sleep(5)
        self.last_processes_info_created = datetime.now()
        self.processes_info(active_processes, finished_processes_keys_list, finished_processes_multithread_list)

        if finished_processes_multithread_list:
            self.logger.info(finished_processes_multithread_list[0][0])

            with ThreadPoolExecutor(max_workers=min(self.MAX_THREADS, len(finished_processes))) as executor:
                executor.map(self.multi_check, finished_processes_multithread_list)
        self.logger.info('end of check_working_accounts')
        self.checker_working_accounts_started = False

    def check_timeout_process(self):
        all_processes = {k: v for k, v in list(self.working_accounts_data.items())}
        all_processes_multithread_list = [[k, v] for k, v in all_processes.items()]
        if all_processes_multithread_list:

            with ThreadPoolExecutor(max_workers=min(self.MAX_THREADS, len(all_processes))) as executor:
                executor.map(self.check_timeout, all_processes_multithread_list)

        self.checker_timeout_process = False

    def check_timeout(self, item):
        serial, answer = item[0], item[1]
        if answer:
            self.logger.info(f'current start_time for {serial} is {answer.start_time}, time now - {datetime.now()}, deadline is - {answer.start_time + timedelta(minutes=60)}, is_timeout - {answer.start_time <= datetime.now() - timedelta(minutes=60)}')
            if answer.start_time <= datetime.now() - timedelta(minutes=self.CONFIG.iteration_timeout_min):
                self.logger.error(f'timeout for process of device {serial}, finish')
                # вынести в статистику кол-во process_timeout за час
                answer.device_info.params['process_timeout'] = True
                # for process in multiprocessing.active_children():
                #     if process.name == serial:
                #         process.terminate()
                #         process.join()
                self.multi_check(item)

    def multi_check(self, item):
        try:
            self.logger.info('multi_check проход')
            serial, answer = item[0], item[1]
            try:
                process = [p for p in self.working_accounts_processes if p.name == serial][0]
            except Exception as e:
                self.logger.exception(f'multi_check: не найден был процесс девайса {serial}')
                sentry_sdk.capture_exception(e)
                return
            if answer:
                self.logger.info(f'{serial} multi_check answer: {answer.task}')
                if answer.task == 'reg':
                    self.logger.info(f'device {serial} registered account {"successfully!" if answer.account.registered else "un-successfully!"}')
                    self.logger.info(f'answer.account.registered is {answer.account.registered}')
                    if answer.account.registered:
                        if answer.account.phone is None:
                            if not answer.account.phone:
                                self.logger.info(f"Девайс {serial} отсылает phone none на роут insert_account")
                            self.logger.error(f"Попытка отправить phone=null на роут insert_account c устройства {serial}")
                        answer.account.id = db.insert_account(account=answer.account, campaign=answer.campaign)
                        db.set_account_in_work(account=answer.account, in_work=False) # Будут появлятся новые застрявшие ак после рега уберу
                    answer.id = db.insert_iteration(type=answer.task, serial=answer.device_info.serial, campaign_id=answer.campaign.id, account_id=answer.account.id, ip=answer.device_info.ip, reinstall_wa=answer.options.reinstall_wa, reg_aggregator=answer.options.code_activator.NAME, reg_country=answer.options.code_activator.region, reg_operator=answer.options.code_activator.operator, reg_phones_used=0, device_info=answer.device_info.params)
                    self.logger.info(f'{serial} multi_check after reg')
                elif answer.task == 'send':
                    self.logger.info(f'device {serial} (ACCOUNT#{answer.account.id}) sent {len(answer.messages.messages_sent)} messages' + (f' \\w {"ban!" if answer.account.banned else "error!"}' if len(answer.messages.messages_to_send) != 0 else '!'))
                    self.logger.info(f'device {serial} - start update')
                    db.update_account(answer.account)
                    self.logger.info(f'device {serial} - end update')
                    self.logger.info(f'device {serial} - start insert')
                    answer.id = db.insert_iteration(type=answer.task, serial=answer.device_info.serial, campaign_id=answer.campaign.id, account_id=answer.account.id, ip=answer.device_info.ip, reinstall_wa=answer.options.reinstall_wa, device_info=answer.device_info.params)
                    self.logger.info(f'device {serial} - end insert')
                    self.logger.info(f'{serial} multi_check after send')
                elif answer.task == 'scan':
                    self.logger.info(f'device {serial} (ACCOUNT#{answer.account.id}) finished scan' + (f' \\w {"ban!" if answer.account.banned else "error!"}' if not answer.account.web_backup or answer.account.banned else '!'))
                    db.update_account(answer.account)
                    answer.id = db.insert_iteration(type=answer.task, serial=answer.device_info.serial, campaign_id=answer.campaign.id, account_id=answer.account.id, ip=answer.device_info.ip, reinstall_wa=answer.options.reinstall_wa, device_info=answer.device_info.params)
                    self.logger.info(f'{serial} multi_check after scan')

                if answer.account.banned and (answer.account.registered or answer.task in ('send', 'scan')):
                    self.logger.info(f'{serial} multi_check set bans')
                    db.set_account_banned(answer.account)
                for i, message in enumerate(answer.messages.messages_income):
                    answer.messages.messages_income[i]['answer'] = 1

                self.logger.info(f'{serial} multi_check before insert messages')
                # Та же самая логика только для ботов
                bots_messages_sent = list(filter(lambda x: x['id'] == 0, answer.messages.messages_sent))
                bots_messages_not_sent = list(filter(lambda x: x['id'] == 0, answer.messages.messages_to_send))
                warm_phones_not_valid = list(filter(lambda x: x['id'] == 0, answer.messages.messages_not_valid))

                db.insert_outcome_messages(bots_messages_sent, answer.id, is_warm=True)
                db.update_warm_not_valid_phones(warm_phones_not_valid)
                db.update_warm_not_sent_messages(bots_messages_not_sent)
                self.logger.info(f'{serial} multi_check after bots messages')

                # На боевые
                db.insert_outcome_messages(answer.messages.messages_sent, answer.id)
                db.insert_income_messages(answer.messages.messages_income, answer.id)
                db.update_not_valid_phones(answer.messages.messages_not_valid)
                db.update_not_sent_messages(answer.messages.messages_to_send)
                self.logger.info(f'{serial} multi_check after all messages')

                # Удаление фоток групп или коммьюнити (если они есть) после итерации
                utils.GroupImage.delete(serial)
                self.logger.info(f'{serial} multi_check after deleting images')

                # if answer.task == 'send' and not self.stopped and not answer.account.banned:
                #     messages = db.find_answers(answer.messages.messages_income, answer.campaign.id, domain=self.CONFIG.links_domain, account_name=answer.account.name.split(' ')[0])
                #     if messages:
                #         del self.working_accounts_data[serial]
                #         self.logger.info(f'device {serial} (ACCOUNT#{answer.account.id}) launching: sending {len(messages.messages_to_send)} answers with {answer.campaign.messages_breaktime_min}-{answer.campaign.messages_breaktime_min + answer.campaign.messages_breaktime_rand}s timeout')
                #         self.launch_session(task='send', serial=serial, campaign=answer.campaign, account=answer.account, messages=messages)
                #         continue
                if answer.task in ('send', 'scan'):
                    self.logger.info(f'{serial} multi_check set account in work')
                    db.set_account_in_work(account=answer.account, in_work=False)
                self.logger.info(f"multi_check start delete working_accounts_data for {serial}")
                del self.working_accounts_data[serial]
                self.logger.info(f"multi_check end delete working_accounts_data for {serial}")
                if self.stopped:
                    self.logger.info(f'{serial} multi_check if stopped update device')
                    db.update_device(serial=serial, farm=None)
                self.logger.info(f"start check working_accounts_processes")
                for p in self.working_accounts_processes:
                    self.logger.info(f"Start for in working_accounts_processes")
                    if p.name == serial:
                        if p.exitcode == 1:
                            self.logger.warning(f'process of device {serial} crashed, reboot...')
                            # subprocess.call(f"adb -s {serial} reboot", shell=True, stdout=subprocess.DEVNULL)
                            # time.sleep(5)
                        self.logger.info(f"multi_check start remove working_accounts_processes for {p}")
                        self.working_accounts_processes.remove(p)
                        self.logger.info(f"multi_check end remove working_accounts_processes for {p}")
                        self.logger.info(f'{serial}: start join')
                        p.join(timeout=60)
                        if p.is_alive():
                            self.logger.warning("Process start terminate")
                            p.terminate()
                            self.logger.warning("Process end terminate")
                            sentry_sdk.capture_exception(Exception(f'CANT JOIN PROCESS FOR {serial}'))
                        self.logger.info(f'{serial}: end join')
                        break
                self.logger.info(f'iteration by device {serial} inserted')
            else:
                self.logger.error('empty iteration answer!')
                self.working_accounts_processes.remove(process)
                process.join()
                self.logger.info(f'{serial}: end join empty iteration')

                del self.working_accounts_data[serial]
        except Exception as e:
            self.logger.exception(f'Exception in multi_tasks: {e}')

    def start_iterations(self):
        if serials := list(filter(lambda s: s not in self.working_accounts_data, self.devices)):
            self.logger.info(f'start multi thread checker for {len(serials)} process')
            with ThreadPoolExecutor(max_workers=min(self.MAX_THREADS, len(serials))) as executor:
                executor.map(self.check_task_simple, serials)
        self.checker_started = False

    def check_task(self, serial):
        # скан
        if config.ENABLE_WEB_BACKUP:
            account = db.get_account_to_scan_web(serial=serial)
            if account and self.get_bool_from_config(field='scan'):
                if proxy := db.get_proxy(serial=serial, county=account.country):
                    self.launch_web_scan(serial, account, proxy)
                    return
                db.set_account_in_work(account=account, in_work=False)
            elif account:
                self.launch_web_scan(serial, account)
                return
        # рассылка
        else:
            self.logger.info(f'{serial} check_task вошел')
            serial_binding = self.CONFIG.serial_binding[self.mac] if self.CONFIG.serial_binding.get(self.mac) in (True, False) else self.CONFIG.serial_binding['default']
            proxy_status = self.get_bool_from_config(field='send')
            account = db.get_account(serial=serial, farm=self.mac, serial_binding=serial_binding)
            self.logger.info(f'{serial} check_task взял аккаунт')
            if account and proxy_status:
                self.logger.info(f'{serial} check_task аккаунт и прокси статус')

                if proxy := db.get_proxy(serial=serial, country=account.country):
                    self.launch_sending(serial, account, proxy)
                    self.logger.info(f'{serial} check_task аккаунт и прокси статус и прокси')
                    return
                db.set_account_in_work(account=account, in_work=False)
                # если не получили прокси для аккаунта, значит прошлый аккаунт на устройстве уже забанен и можно запрашивать любой другой аккаунт для которого доступна прокси
                if account := db.get_account(serial=serial, farm=self.mac, serial_binding=serial_binding, proxy_enable=True):
                    if proxy := db.get_proxy(serial=serial, country=account.country):
                        self.launch_sending(serial, account, proxy)
                        self.logger.info(f'{serial} check_task аккаунт и прокси статус и аккаунт с proxy_enabled')
                        return
                    #  на случай если прокси кто-то уже забрал
                    db.set_account_in_work(account=account, in_work=False)

                if account := db.get_account(serial=serial, farm='no_proxy', serial_binding=serial_binding):
                    self.launch_sending(serial, account)
                    self.logger.info(f'{serial} check_task аккаунт и прокси статус и аккаунт')
                    return
            elif account:
                self.launch_sending(serial, account)
                self.logger.info(f'{serial} check_task аккаунт')
                return
            elif proxy_status:
                self.logger.info(f'{serial} check_task прокси статус')
                if account := db.get_account(serial=serial, farm='no_proxy', serial_binding=serial_binding):
                    self.launch_sending(serial, account)
                    self.logger.info(f'{serial} check_task прокси статус и аккаунт')
                    return
        # регистрация
        # Автотесты
        self.logger.info(f'{serial} check_task переход к взятию кампании')
        is_campaign_test = False
        if self.CONFIG.campaign_test:
            is_campaign_test = self.CONFIG.campaign_test.get(self.mac).get('reg') if self.CONFIG.campaign_test.get(self.mac) else self.CONFIG.campaign_test.get('default').get('reg')

        campaign = db.get_campaign_to_reg(serial=serial, farm=self.mac, is_campaign_test=is_campaign_test)
        self.logger.info(f'{serial} check_task взял кампанию')
        proxy_status = self.get_bool_from_config(field='reg')
        if campaign and proxy_status:
            self.logger.info(f'{serial} check_task кампания и прокси статус')
            if proxy := db.get_proxy(serial=serial, campaign_id=campaign.id):
                self.launch_registration(serial, campaign, proxy)
                self.logger.info(f'{serial} check_task кампания и прокси статус и прокси')
                return
            if campaign := db.get_campaign_to_reg(serial=serial, farm='no_proxy', is_campaign_test=is_campaign_test):
                self.launch_registration(serial, campaign)
                self.logger.info(f'{serial} check_task кампания и прокси статус и кампания')
                return
        elif campaign:
            self.launch_registration(serial, campaign)
            self.logger.info(f'{serial} check_task кампания')
            return
        else:
            if campaign := db.get_campaign_to_reg(serial=serial, farm='no_proxy', is_campaign_test=is_campaign_test):
                self.launch_registration(serial, campaign)
                self.logger.info(f'{serial} check_task кампания no_proxy')
                return
        self.logger.info(f'device {serial} have no task')

    def check_task_simple(self, serial):
        # скан
        if config.ENABLE_WEB_BACKUP:
            account = db.get_account_to_scan_web(serial=serial)
            if account and self.get_bool_from_config(field='scan'):
                if proxy := db.get_proxy(serial=serial, county=account.country):
                    self.launch_web_scan(serial, account, proxy)
                    return
                db.set_account_in_work(account=account, in_work=False)
            elif account:
                self.launch_web_scan(serial, account)
                return
        # рассылка
        else:
            self.logger.info(f'{serial} check_task вошел')
            serial_binding = self.CONFIG.serial_binding[self.mac] if self.CONFIG.serial_binding.get(self.mac) in (True, False) else self.CONFIG.serial_binding['default']
            proxy_status = self.get_bool_from_config(field='send')
            self.logger.info(f'{serial} check_task взял аккаунт')
            if proxy_status:
                self.logger.info(f'{serial} check_task прокси статус')
                if account := db.get_account(serial=serial, farm='no_proxy', serial_binding=serial_binding):
                    self.launch_sending(serial, account)
                    self.logger.info(f'{serial} check_task прокси статус и аккаунт')
                    return
        # регистрация
        # Автотесты
        self.logger.info(f'{serial} check_task переход к взятию кампании')
        is_campaign_test = False
        if self.CONFIG.campaign_test:
            is_campaign_test = self.CONFIG.campaign_test.get(self.mac).get('reg') if self.CONFIG.campaign_test.get(self.mac) else self.CONFIG.campaign_test.get('default').get('reg')
        self.logger.info(f'{serial} check_task взял кампанию')
        if campaign := db.get_campaign_to_reg(serial=serial, farm='no_proxy', is_campaign_test=is_campaign_test):
                self.launch_registration(serial, campaign)
                self.logger.info(f'{serial} check_task кампания no_proxy')
                return
        self.logger.info(f'device {serial} have no task')

    def check_wa_installed(self):
        apk_folder = f'{os.getcwd()}/apk'

        if self.CONFIG.wa_version not in os.listdir(apk_folder):
            self.logger.info(f'download whatsapp apk')
            SelectelCDN().download_file(self.CONFIG.wa_version, apk_folder, 'yandex/apk')


    def run(self):
        try:
            while True:
                self.get_db_config()
                self.check_wa_installed()

                self.check_devices()

                if self.CONFIG.enable_new_iters and not self.checker_started:
                    self.logger.info("checking devices to get task")
                    self.checker_started = True
                    self.start_iterations()
                    self.logger.info('After start_iterations()')

                if not self.checker_working_accounts_started:
                    self.logger.info('checker_working_accounts_started()')
                    # self.logger.info("checking devices to finish task")
                    self.checker_working_accounts_started = True
                    self.check_working_accounts()

                # скорее всего больше не нужно
                if not self.checker_timeout_process:
                    self.logger.info('checker_timeout_process()')
                    # self.logger.info("checking process on timeout")
                    self.checker_timeout_process = True
                    self.check_timeout_process()

                self.check_can_be_stop()

        except (Exception, KeyboardInterrupt) as error:
            traceback.print_exc()
            sentry_sdk.capture_exception(error) # Для 100% лога в sentry
            self.stopped = True
            while self.working_accounts_data:
                self.check_working_accounts()


if __name__ == "__main__":
    # святой грааль
    multiprocessing.set_start_method('spawn')
    main = Main()
    main.run()
