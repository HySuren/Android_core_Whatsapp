import base64
import logging
from datetime import datetime, timedelta
from io import BytesIO
import os
import random
import subprocess
import time

from PIL import Image
import sentry_sdk
from uiautomator2.exceptions import UiObjectNotFoundError

import config
from core import script_iterator
import core.exceptions
from scrip_iterations_rules import phone_preparation
from services import utils, backup, photos
from services.code_activators import exceptions as code_activator_exceptions, ACTIVATORS_NAMES_DICT
from services.photos.photos_manager import PHONE_IMAGES_FOLDER, SAVE_IMG_PATH
from services.utils import get_wa_contacts, set_proxy
from services.web_backup import BackupService, BackupServiceException, BackupExistsException
from requests import Timeout

sentry_sdk.init(dsn="https://a32fb9b2252544609dbe4f6d882825f4@sentry.caltat.com/5")


def do_nothing(obj: script_iterator.ScriptIterator):
    ...

def click_home(obj: script_iterator.ScriptIterator) -> None:
    obj.d.keyevent('home')

def reset_wa(obj: script_iterator.ScriptIterator):
    if obj.proxy and (not obj.proxy_ready or obj.proxy.change):
        if obj.wa_ready:
            obj.d.app_stop(obj.app)
        obj.d.app_start('org.sandroproxy.drony')
    elif not obj.wa_ready:
        if obj.restore_backup:

            if not obj.options.reinstall_wa and obj.d.shell(f'pm list packages | grep {obj.app}').output == '':
                obj.logger.warning(f'no WhatsApp on device, installing ...')
                obj.options.reinstall_wa = True

            if obj.options.reinstall_wa:
                obj.d.shell("pm uninstall com.whatsapp")
                obj.d.shell("pm uninstall com.whatsapp.w4b")
                obj.d.shell("rm -rf /data/local/tmp/*")
                if obj.app == 'com.whatsapp.w4b':
                    subprocess.call(f"adb -s {obj.serial} install -d apk/wab2.22.24.78.apk", shell=True, stdout=subprocess.DEVNULL)
                else:
                    obj.logger.info('installing apk')
                    if obj.d.shell(f'pm list packages | grep {obj.app}').output != '':
                        obj.logger.warning('whatsapp installed before install')
                        obj.d.shell("pm uninstall com.whatsapp")
                    for x in range(5):
                        try:
                            answer = subprocess.run(f'adb -s {obj.serial} install -d apk/{obj.wa_version}', shell=True, capture_output=True, timeout=120, text=True).stdout
                            obj.logger.info(f'GOOD {answer}')
                        except subprocess.TimeoutExpired as e:
                            if obj.d.shell(f'pm list packages | grep {obj.app}').output == '':
                                obj.logger.warning('cant install whatsapp, retry')
                                continue
                            else:
                                obj.logger.info(f'whatsapp installed but error occurred: {e}')
                                obj.wa_ready = True
                                break
                        obj.wa_ready = True
                        break
                    if not obj.wa_ready:
                        obj.logger.error('cant install whatsapp 5 times')
                        raise core.exceptions.NoWhatsappException

                obj.d.shell(f'su -c "magisk --denylist add {obj.app}"')

            obj.d.shell(f"pm clear {obj.app}")

            if obj.account.backup:
                backup.restore.restore_dump(obj.serial, obj.account.backup, obj.app, obj.cdn)
                obj.d.shell(f'fallocate -l 1M {config.PHONE_TMP_FOLDER}/backup_{obj.account.backup}')

            if obj.campaign.parameters['grant_wa_permissions']:
                obj.d.shell(f"pm grant {obj.app} android.permission.READ_CALL_LOG")
                obj.d.shell(f"pm grant {obj.app} android.permission.ACCESS_FINE_LOCATION")
                obj.d.shell(f"pm grant {obj.app} android.permission.ANSWER_PHONE_CALLS")
                obj.d.shell(f"pm grant {obj.app} android.permission.READ_PHONE_NUMBERS")
                obj.d.shell(f"pm grant {obj.app} android.permission.RECEIVE_SMS")
                obj.d.shell(f"pm grant {obj.app} android.permission.READ_EXTERNAL_STORAGE")
                obj.d.shell(f"pm grant {obj.app} android.permission.ACCESS_COARSE_LOCATION")
                obj.d.shell(f"pm grant {obj.app} android.permission.READ_PHONE_STATE")
                obj.d.shell(f"pm grant {obj.app} android.permission.SEND_SMS")
                obj.d.shell(f"pm grant {obj.app} android.permission.CALL_PHONE")
                obj.d.shell(f"pm grant {obj.app} android.permission.WRITE_CONTACTS")
                obj.d.shell(f"pm grant {obj.app} android.permission.CAMERA")
                obj.d.shell(f"pm grant {obj.app} android.permission.GET_ACCOUNTS")
                obj.d.shell(f"pm grant {obj.app} android.permission.WRITE_EXTERNAL_STORAGE")
                obj.d.shell(f"pm grant {obj.app} android.permission.RECORD_AUDIO")
                obj.d.shell(f"pm grant {obj.app} android.permission.READ_CONTACTS")

        obj.wa_ready = True
        obj.d.app_start(obj.app)
    elif not obj.account.backup and obj.task == 'reg' and obj.account.registered:
        obj.logger.info('backuping whatsapp')
        obj.d.app_stop(obj.app)
        phone_preparation.turn_airplane_mode(obj.d, on=True)
        obj.logger.info(f'creating backup...')
        for _ in range(10):
            try:
                obj.account.backup = backup.create.create_dump(obj.serial, obj.app, obj.cdn)
                break
            except Exception as e:
                pass
        obj.d.shell(f'fallocate -l 1M {config.PHONE_TMP_FOLDER}/backup_{obj.account.backup}')
        obj.logger.info(f'backup created!')
        raise core.exceptions.StopThreadException


def accept_eula(obj: script_iterator.ScriptIterator):
    display = utils.get_display(obj.d)
    description_next = display.get('resource-id', f'{obj.app}:id/next_button')
    if description_next.exists:
        obj.d(resourceId=f"{obj.app}:id/next_button").click()
        time.sleep(1)
    display2 = utils.get_display(obj.d)
    description_accept = display2.get('resource-id', f'{obj.app}:id/eula_accept')
    if description_accept.exists:
        obj.d(resourceId=f'{obj.app}:id/eula_accept').click()


def enter_reg_phone(obj: script_iterator.ScriptIterator):
    if not obj.start_reg_timestamp:
        obj.start_reg_timestamp = time.time()
        obj.finish_reg_timestamp = obj.start_reg_timestamp + obj.campaign.parameters['reg_seconds_timeout']

    if obj.device_info.params.get('business_account'):
        del obj.device_info.params['business_account']
    if obj.account.name:
        obj.account.banned = True
        raise core.exceptions.BanException

    if not obj.account.phone:
        if obj.reg_phones_entry_limit == 0:
            raise core.exceptions.StopThreadException

        # если одна страна на итерацию
        if obj.campaign.one_country_iter:
            _reg_one_country(obj)
        else:
            _reg_legacy(obj)

        obj.reg_phones_entry_limit -= 1
        obj.d(resourceId=f'{obj.app}:id/registration_cc').set_text(obj.phone_code)
        obj.d(resourceId=f'{obj.app}:id/registration_phone').set_text(obj.phone_num)
        obj.d(resourceId=f'{obj.app}:id/registration_submit').click()


def _reg_legacy(obj: script_iterator.ScriptIterator):
    count = len(obj.options.reg_aggregators)
    tries = obj.country_tries * count
    while True:
        if tries % count == 0:
            time.sleep(int(10 / count))
        tries -= 1
        activator = obj.options.reg_aggregators.pop(0)
        obj.options.reg_aggregators.append(activator)

        try:
            obj.options.code_activator = ACTIVATORS_NAMES_DICT[activator.name](activator.operators, activator.country)
            obj.account.activate_service_id, obj.phone_code, obj.phone_num = obj.options.code_activator.get_phone()
            obj.account.phone = obj.phone_code + obj.phone_num
            if not obj.device_info.params.get('phones_used'):
                obj.device_info.params['phones_used'] = []
                obj.device_info.params['temporary_ban'] = 0
                obj.device_info.params['not_received'] = 0
            obj.device_info.params['phones_used'].append(obj.account.phone)
            obj.options.code_activator.sms_confirm(obj.account.activate_service_id)
            obj.logger.info(f'got phone {obj.account.phone}')
            break

        except code_activator_exceptions.PhoneActivationException:
            obj.logger.warning(f'no phone returned by {activator.name}!')
            if tries <= 0:
                raise core.exceptions.StopThreadException


def _reg_one_country(obj: script_iterator.ScriptIterator):
    if not obj.device_info.params.get('phones_used'):
        obj.device_info.params['phones_used'] = []
        obj.device_info.params['temporary_ban'] = 0
        obj.device_info.params['not_received'] = 0
    tries = 0
    while True:
        if time.time() >= obj.finish_reg_timestamp:
            obj.logger.info('no phones from reg_aggregators, finish')
            raise core.exceptions.StopThreadException
        # TODO
        #  ОТРЕФАЧИТЬ ЭТУ ХУЙНЮ
        if not obj.tmp_reg_aggregators and obj.all_countries and not obj.device_info.params['phones_used'] and tries < 1:
            obj.country = obj.all_countries.pop(0)
            obj.all_countries.append(obj.country)
            reg_aggregators_for_country = list(filter(lambda s: s.country == obj.country, obj.options.reg_aggregators))
            obj.tmp_reg_aggregators = random.sample(reg_aggregators_for_country, len(reg_aggregators_for_country))
            obj.current_activator = obj.tmp_reg_aggregators.pop(0)
            tries = obj.country_tries
            obj.logger.info(f'trying to reg {obj.country} from {obj.current_activator}')
        elif obj.device_info.params['phones_used'] and not obj.tmp_reg_aggregators:
            obj.country = obj.current_activator.country
            reg_aggregators_for_country = list(filter(lambda s: s.country == obj.country, obj.options.reg_aggregators))
            obj.tmp_reg_aggregators = random.sample(reg_aggregators_for_country, len(reg_aggregators_for_country))
            obj.current_activator = obj.tmp_reg_aggregators.pop(0)
            tries = obj.country_tries
            obj.logger.info(f'trying to reg only {obj.country} from {obj.current_activator}')
        elif (not obj.all_countries or obj.device_info.params['phones_used']) and not obj.tmp_reg_aggregators and tries < 1:
            obj.logger.info('no aggregators, finish reg')
            raise core.exceptions.StopThreadException

        time.sleep(3)
        if tries < 1 and obj.tmp_reg_aggregators:
            obj.current_activator = obj.tmp_reg_aggregators.pop(0)
            obj.logger.info(f'trying to reg {obj.country} from {obj.current_activator}')
            tries = obj.country_tries
        tries -= 1
        try:
            obj.options.code_activator = ACTIVATORS_NAMES_DICT[obj.current_activator.name](obj.current_activator.operators, obj.current_activator.country)
            reg_aggregator_name = f'{obj.options.code_activator.NAME}_{obj.current_activator.country}'
            if free_price_dict := obj.campaign.parameters['free_price_dict'].get(reg_aggregator_name):
                if obj.options.code_activator.NAME in obj.activators_with_responses:
                    obj.account.activate_service_id, obj.phone_code, obj.phone_num = obj.options.code_activator.get_phone(obj=obj, free_price=free_price_dict['free_price'], max_free_price=free_price_dict['max_free_price'], free_price_array=free_price_dict['free_price_array'])
                else:
                    obj.account.activate_service_id, obj.phone_code, obj.phone_num = obj.options.code_activator.get_phone(free_price=free_price_dict['free_price'], max_free_price=free_price_dict['max_free_price'], free_price_array=free_price_dict['free_price_array'])
            elif obj.options.code_activator.NAME in obj.activators_with_responses:
                obj.logger.info(f'requesting phone for {obj.country} from {obj.current_activator}')
                obj.account.activate_service_id, obj.phone_code, obj.phone_num = obj.options.code_activator.get_phone(obj=obj)
                obj.logger.info(f'phone requested for {obj.country} from {obj.current_activator}')
            else:
                obj.account.activate_service_id, obj.phone_code, obj.phone_num = obj.options.code_activator.get_phone()
            obj.account.phone = obj.phone_code + obj.phone_num

            obj.device_info.params['phones_used'].append(obj.account.phone)
            obj.logger.info(f'trying confirm phone for {obj.country} from {obj.current_activator}')
            obj.options.code_activator.sms_confirm(obj.account.activate_service_id)
            obj.logger.info(f'got phone {obj.account.phone}')
            break

        except Exception as e:
            if isinstance(e, code_activator_exceptions.PhoneActivationException):
                obj.logger.warning(f'no phone returned by {obj.current_activator.name}!')
            elif isinstance(e, Timeout):
                obj.logger.warning(f'timeout on request for {obj.current_activator.name}!')
            else:
                raise e


def _call_warmup(obj: script_iterator.ScriptIterator):
    """ Логика прогрева звонками """

    if obj.calls_finished:
        obj.d.keyevent('back')
    while obj.messages.messages_to_send and len(obj.messages.messages_sent) < obj.call_times:
        display = utils.get_display(obj.d)
        phone = utils.normalize_phone(display.get('resource-id', f'{obj.app}:id/conversation_contact_name').text)
        find_to = datetime.now() + timedelta(seconds=1)

        while datetime.now() < find_to and obj.messages.messages_to_send[0]['phone'] != phone:
            display = utils.get_display(obj.d)
            phone = utils.normalize_phone(display.get('resource-id', f'{obj.app}:id/conversation_contact_name').text)

        if obj.messages.messages_to_send[0]['phone'] != phone:
            if obj.last_sent and obj.had_incoming_call:
                obj.d(description="Voice call").click()
                obj.had_incoming_call = False
                time.sleep(10)

        if obj.messages.messages_to_send[0]['phone'] == phone:
            try:
                obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
                obj.last_sent = datetime.now()

                if obj.d(resourceId=f"{obj.app}:id/call_notification_title").exists:
                    obj.d(resourceId=f"{obj.app}:id/call_notification_title").click()
                    time.sleep(2)

                # Странная херня у особенных пользователей
                if obj.d(description="Call").exists:
                    obj.d(description="Call").click()
                    time.sleep(1)
                    obj.d(resourceId=f"{obj.app}:id/audio_call_item").click()

                obj.logger.info('Start call')
                obj.d(description="Voice call").click()
                time.sleep(3)
                if obj.d(description="Voice call").info.get('enabled'):
                    obj.d(description="Voice call").click()
                else:
                    obj.d(resourceId=f"{obj.app}:id/call_notification_title").click()
                time.sleep(10)
            except UiObjectNotFoundError:
                obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_ok').click()
                if obj.d(resourceId=f"{obj.app}:id/call_notification_title").exists:
                    obj.d(resourceId=f"{obj.app}:id/call_notification_title").click()
                    time.sleep(5)
                obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
                obj.last_sent = datetime.now()
                obj.logger.info('Start call')

                if obj.d(description="Voice call").info.get('enabled'):
                    obj.d(description="Voice call").click()
                else:
                    obj.d(resourceId=f"{obj.app}:id/call_notification_title").click()
                time.sleep(10)

        elif display.get('resource-id', f'{obj.app}:id/ephemeral_nux_ok').text == 'OK':
            obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_ok').click()

        if obj.campaign.parameters['timeout_after_send']:
            time.sleep(obj.campaign.parameters['timeout_after_send'])

        if obj.messages.messages_to_send:
            if (obj.messages.messages_to_send[0]).get('image') is None:
                obj.d.shell(
                    f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' +
                    obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (
                    obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + f'" -p {obj.app}')
            else:
                obj.d.shell(
                    f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' +
                    obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (
                    obj.messages.messages_to_send[0]['message']).replace('"',
                                                                         '\\"') + f'" -p {obj.app}' + f' --eu android.intent.extra.STREAM file:///{PHONE_IMAGES_FOLDER}/tmp_photo_{obj.account.id}.jpg')
                time.sleep(1)


def _bot_warmup(obj: script_iterator.ScriptIterator):
    """ Логика прогрева ботами """

    while 0 in [message['id'] for message in obj.messages.messages_to_send]:
        if obj.without_internet_w_warm and (
                (obj.bots_enable and len(obj.messages.messages_sent) >= obj.bots_amount) or (obj.calls_enabled and len(
                obj.messages.messages_sent) >= obj.call_times or obj.first_calls_enabled)) and not obj.campaign.without_internet:
            phone_preparation.turn_airplane_mode(obj.d, on=True)
            obj.campaign.without_internet = True
            obj.device_info.params['without_internet'] = True
        find_to = datetime.now() + timedelta(seconds=1)
        display = utils.get_display(obj.d)
        phone = utils.normalize_phone(display.get('resource-id', f'{obj.app}:id/conversation_contact_name').text)

        while datetime.now() < find_to and (
                obj.messages.messages_to_send[0]['phone'] != phone or display.get('resource-id',
                                                                                  f'{obj.app}:id/entry').text == 'Message'):
            display = utils.get_display(obj.d)
            phone = utils.normalize_phone(display.get('resource-id', f'{obj.app}:id/conversation_contact_name').text)

        # if display.get('resource-id', f'{obj.app}:id/entry').text != 'Message':
        if obj.messages.messages_to_send[0]['phone'] == phone and display.get('resource-id',
                                                                              f'{obj.app}:id/entry').text != 'Message':
            if obj.last_sent:
                if obj.bots_enable and obj.bots_pause_enable and len(obj.messages.messages_sent) < obj.bots_amount:
                    sleep_to = obj.last_sent + timedelta(
                        seconds=(obj.bots_breaktime_min + random.randint(0, obj.bots_breaktime_rand)))
                else:
                    sleep_to = obj.last_sent + timedelta(seconds=(obj.options.messages_breaktime_min + random.randint(0,
                                                                                                                      obj.options.messages_breaktime_rand)))
                while datetime.now() < sleep_to:
                    if obj.campaign.read_messages:
                        obj.messages.messages_income = utils.get_wa_answers(obj.d)
                    time.sleep(1)
            try:
                obj.d(resourceId=f'{obj.app}:id/send_container').click()
                obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
                obj.last_sent = datetime.now()
            except UiObjectNotFoundError:
                if obj.d(resourceId=f"{obj.app}:id/ephemeral_nux_dismiss").exists:
                    obj.d(resourceId=f"{obj.app}:id/ephemeral_nux_dismiss").click()
                obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_ok').click()
                obj.d(resourceId=f'{obj.app}:id/send_container').click()
                obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
                obj.last_sent = datetime.now()

        elif display.get('resource-id', f'{obj.app}:id/ephemeral_nux_ok').text == 'OK':
            obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_ok').click()

        if obj.campaign.parameters['timeout_after_send']:
            time.sleep(obj.campaign.parameters['timeout_after_send'])

        if obj.messages.messages_to_send:
            if (obj.messages.messages_to_send[0]).get('image') is None:
                obj.d.shell(
                    f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' +
                    obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (
                    obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + f'" -p {obj.app}')
            else:
                obj.d.shell(
                    f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' +
                    obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (
                    obj.messages.messages_to_send[0]['message']).replace('"',
                                                                         '\\"') + f'" -p {obj.app}' + f' --eu android.intent.extra.STREAM file:///{PHONE_IMAGES_FOLDER}/tmp_photo_{obj.account.id}.jpg')
                time.sleep(1)
    else:
        obj.bots_finished = True


def not_valid(obj: script_iterator.ScriptIterator):
    obj.account.phone = None
    obj.phone_code = None
    obj.phone_num = None
    obj.d(resourceId="android:id/button1").click()


def accept_reg_phone(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_banned_reg_phone(obj: script_iterator.ScriptIterator):
    obj.options.code_activator.phone_ban(obj.account.activate_service_id)
    if obj.options.retry_bad_phone > 0:
        obj.logger.warning(f'ban during registration, retying with new phone ...')
        obj.options.retry_bad_phone -= 1
        obj.account.phone = None
        obj.account.name = None
        obj.phone_code = None
        obj.phone_num = None
        obj.d(resourceId='android:id/button2').click()
    else:
        raise core.exceptions.BanException


def choose_sms_reg_verify(obj: script_iterator.ScriptIterator):
    time.sleep(2)
    if obj.d(text="SEND SMS").exists:
        obj.d(text="SEND SMS").click()
    display = utils.get_display(obj.d)
    description_verify = display.get('resource-id', f"{obj.app}:id/verify_with_sms_button")
    description_verify_another = display.get('text', f"VERIFY ANOTHER WAY")
    if description_verify.exists:
        obj.d(resourceId=f"{obj.app}:id/verify_with_sms_button").click()
        if obj.d(text="SEND SMS").exists:
            obj.d(text="SEND SMS").click()
    elif description_verify_another.exists:
        obj.d(text='VERIFY ANOTHER WAY').click()
        time.sleep(2)
        obj.d(text="SEND SMS").click()
    else:
        obj.logger.error('cant find any sms-verify button')
        raise core.exceptions.StopThreadException


def handle_switching_business(obj: script_iterator.ScriptIterator):
    # obj.device_info.params['business_account'] = True
    obj.d(resourceId="android:id/button1").click()


def enter_reg_code_or_go_back(obj: script_iterator.ScriptIterator):
    is_not_valid_phone = False
    if obj.account.phone and not obj.account.code:
        display = utils.get_display(obj.d)
        description = display.get('resource-id', f'{obj.app}:id/send_code_description')
        description2 = display.get('resource-id', f'{obj.app}:id/verify_wa_old_content_subtitle')
        is_not_valid_phone = (description2.exists and description2.text == 'Open WhatsApp on your other phone to get the 6-digit code.')
        #  если номер невалиден для регистрации
        if is_not_valid_phone or (description.exists and (utils.replace_phone(description.text, use_normalize=True) == "Can't send an SMS with your code because you've tried to register {phone_replaced} recently. Request a call or wait before requesting an SMS. Wrong number?" or utils.replace_phone(description.text, use_normalize=True) == "You've tried to register {phone_replaced} recently. Wait before requesting an SMS or a call with your code.")):

            obj.account.phone = None
            obj.phone_code = None
            obj.phone_num = None
            obj.device_info.params['temporary_ban'] += 1
        #  для регистрации через звонки, попадаем сюда при первой попытке запросить код + все последующие
        elif obj.options.code_activator.NAME in config.CODE_ACTIVATORS_W_CALLS and not obj.code_requested:
            _inner_enter_reg_code(obj, 1)
        #  если код уже запрошен в первый раз или если надо попробовать запросить код еще раз
        elif obj.options.code_activator.NAME in config.CODE_ACTIVATORS_W_CALLS and obj.code_requested and obj.code_requested_counter < 3:
            try:
                obj.account.code = obj.options.code_activator.get_code(obj.account.activate_service_id, timeout=obj.options.timeout_getting_code_calls)
            except code_activator_exceptions.PhoneActivationException:
                obj.logger.info(f'no code returned by {obj.options.code_activator.NAME}')
                obj.device_info.params['not_received'] += 1
            if obj.account.code:
                obj.device_info.params['tries_code_request'] = obj.code_requested_counter
                obj.d.set_fastinput_ime(False)
                obj.d.shell(f'ime set com.samsung.android.honeyboard/.service.HoneyBoardService')
                if display.get('content-desc', 'Enter 6-digit code').exists:
                    obj.d(description="Enter 6-digit code").set_text(obj.account.code)
                else:
                    obj.d(resourceId=f'{obj.app}:id/verify_sms_code_input').set_text(obj.account.code)
            else:
                obj.code_requested = False
                obj.request_again = True
        #  рега через смс
        else:
            try:
                obj.account.code = obj.options.code_activator.get_code(obj.account.activate_service_id, timeout=obj.options.timeout_getting_code)
                obj.d.set_fastinput_ime(False)
                obj.d.shell(f'ime set com.samsung.android.honeyboard/.service.HoneyBoardService')
                if display.get('content-desc', 'Enter 6-digit code').exists:
                    obj.d(description="Enter 6-digit code").set_text(obj.account.code)
                else:
                    obj.d(resourceId=f'{obj.app}:id/verify_sms_code_input').set_text(obj.account.code)
            except code_activator_exceptions.PhoneActivationException:
                obj.account.phone = None
                obj.phone_code = None
                obj.phone_num = None
                obj.device_info.params['not_received'] += 1

    #  для повторного запроса кода
    if obj.account.phone and not obj.account.code and obj.options.code_activator.NAME in config.CODE_ACTIVATORS_W_CALLS and not obj.code_requested and obj.request_again and obj.code_requested_counter < 3:
        _inner_enter_reg_code(obj, 2)

    if not obj.account.phone:
        obj.options.code_activator.phone_ban(obj.account.activate_service_id)
        if obj.options.retry_bad_phone > 0:
            obj.options.retry_bad_phone -= 1
            obj.account.phone = None
            obj.phone_code = None
            obj.phone_num = None
            obj.code_requested_counter = 0
            obj.request_again = False
            obj.code_requested = False
            obj.logger.warning(f'ban during registration, retying with new phone ...')
            obj.account.name = None
            if is_not_valid_phone:
                obj.d.press('back')
                obj.d.press('back')
            elif obj.options.code_activator.NAME in config.CODE_ACTIVATORS_W_CALLS:
                obj.d.press('back')
                obj.d(description="Wrong number?").click()
            else:
                obj.d(description="Wrong number?").click()

        else:
            obj.logger.warning(f'too many bad phones')
            raise core.exceptions.StopThreadException


#  вложенная функция для реги через звонки
def _inner_enter_reg_code(obj: script_iterator.ScriptIterator, place: int):
    display = utils.get_display(obj.d)
    timer_outer = display.get('resource-id', f'{obj.app}:id/smallest_count_down_time_text')
    if timer_outer.exists:
        # пример текста "You may request a new code in 13:44"
        timer_text = timer_outer.text.split()
        if ':' in timer_text[-1]:
            minutes, seconds = timer_text[-1].split(':')
            timer = int(minutes) * 60 + int(seconds)
        else:
            timer = 181
        if timer <= 180:
            time.sleep(timer + 1)
        else:
            obj.account.phone = None
            obj.phone_code = None
            obj.phone_num = None
            obj.logger.warning('timer too long! o(>ω<)o')

    button = display.get('resource-id', f"{obj.app}:id/fallback_methods_entry_text")
    if button.exists and obj.account.phone:
        obj.d(resourceId=f"{obj.app}:id/fallback_methods_entry_text").click()
        time.sleep(1)
        call = utils.get_display(obj.d).get('resource-id', f"{obj.app}:id/request_otp_code_buttons_layout")
        if call.exists:
            text = call.children[1].text
            if text == 'CALL ME':
                obj.code_requested = True
                obj.code_requested_counter += 1
                obj.d(text='CALL ME').click()
            else:
                timer = text.split()
                if ':' in timer[2]:
                    minutes, seconds = timer[2].split(':')
                    timer = int(minutes) * 60 + int(seconds)
                else:
                    timer = 181
                if timer <= 180:
                    time.sleep(timer + 1)
                    obj.code_requested = True
                    obj.code_requested_counter += 1
                    obj.d(text='CALL ME').click()
                else:
                    obj.account.phone = None
                    obj.phone_code = None
                    obj.phone_num = None
                    obj.logger.warning('timer too long! o(>ω<)o')
        else:
            obj.account.phone = None
            if place == 1:
                obj.logger.warning('cant find menu')
            else:
                obj.logger.warning('cant find  after first request')
    else:
        if obj.account.phone:
            obj.account.phone = None
            if place == 1:
                obj.logger.warning('no button, mb old interface')
            else:
                obj.logger.warning('no button after first request')


def handle_ban_popup_sms(obj: script_iterator.ScriptIterator):
    obj.device_info.params['temporary_ban'] += 1
    obj.account.phone = None
    obj.phone_code = None
    obj.phone_num = None
    obj.d(resourceId='android:id/button1').click()


def handle_ban(obj: script_iterator.ScriptIterator):
    if not obj.account.registered:
        obj.options.code_activator.phone_ban(obj.account.activate_service_id)
    obj.account.banned = True
    raise core.exceptions.BanException


def accept_permission_request(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f'{obj.app}:id/submit').click()


def give_permissions(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f'{obj.app}:id/submit').click()


def allow_permission(obj: script_iterator.ScriptIterator):
    time.sleep(2)
    display = utils.get_display(obj.d)
    if display.get('resource-id', 'com.android.permissioncontroller:id/permission_allow_button').exists:
        obj.d(resourceId='com.android.permissioncontroller:id/permission_allow_button').click()
    elif display.get('resource-id', 'com.android.permissioncontroller:id/permission_allow_foreground_only_button').exists:
        obj.d(resourceId='com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()


def skip_backup(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button2").click()


def enter_reg_name(obj: script_iterator.ScriptIterator, _retry_limit: int = 5):
    if not obj.account.name:
        if obj.app == 'com.whatsapp.w4b' and not obj.tmp_category:
            obj.d(resourceId=f'{obj.app}:id/form_field_main_label_container').click()
        else:
            if obj.options.data_for_account:
                name = obj.options.data_for_account.name
            else:
                name = utils.gen_name()
            for _ in range(_retry_limit):
                try:
                    obj.d(resourceId=f'{obj.app}:id/registration_name').set_text(name)
                    obj.account.name = name
                    obj.d(resourceId=f'{obj.app}:id/register_name_accept').click()
                    return
                except Exception as error:
                    logging.error(f'{obj.serial} - {error}')
                    pass
            obj.d(resourceId=f'{obj.app}:id/registration_name').set_text(name)

def enter_reg_name_spec(obj: script_iterator.ScriptIterator):
    if not obj.account.name:
        if obj.app == 'com.whatsapp.w4b' and not obj.tmp_category:
            obj.d(resourceId=f'{obj.app}:id/form_field_main_label_container').click()
        else:
            if obj.options.data_for_account:
                name = obj.options.data_for_account.name
            else:
                name = utils.gen_name()
            obj.d(resourceId=f'{obj.app}:id/registration_name').set_text(name)

            obj.account.name = name
            obj.d(resourceId=f'{obj.app}:id/register_name_accept').click()


def handle_category(obj: script_iterator.ScriptIterator):
    obj.tmp_category = True
    obj.d(resourceId=f"{obj.app}:id/category_listitem_text").click()


def skip_onboarding(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/onboarding_decline_button").click()

def never_backup(obj: script_iterator.ScriptIterator):
    obj.d(text="Never").click()
    obj.d(resourceId="com.whatsapp:id/gdrive_new_user_setup_btn").click()

def handle_contacts(obj: script_iterator.ScriptIterator):
    if not obj.contacts_refreshed:
        obj.d(resourceId=f'{obj.app}:id/menuitem_overflow').click()
        time.sleep(0.5)
        obj.d(text='Refresh').click()
        time.sleep(10)
        if obj.app == 'com.whatsapp':
            wa_contacts = get_wa_contacts(obj.d)
            valid, not_valid, counter = [], [], 0
            for mess in obj.messages.messages_to_send:
                if mess['phone'] in wa_contacts.keys():
                    counter += 1
            if counter >= len(obj.messages.messages_to_send) * 0.9:
                while obj.messages.messages_to_send:
                    message = obj.messages.messages_to_send.pop(0)
                    try:
                        if wa_contacts[message['phone']] == '1':
                            valid.append(message)
                        elif wa_contacts[message['phone']] == '0':
                            not_valid.append(message)
                        else:
                            obj.logger.info(f'phone not found in wa_contacts!')
                    except KeyError:
                        obj.logger.info(f'phone not found in wa_contacts!')
                obj.device_info.params['valid_contacts'], obj.device_info.params['not_valid_contacts'] = len(valid), len(not_valid)
                obj.messages.messages_to_send, obj.messages.messages_not_valid = random.sample(valid, len(valid)), not_valid
                obj.contacts_refreshed = True
                obj.logger.info(f'validation success!')
                # рассылка с ботами
                if obj.bots_enable:
                    for phone in obj.bots_current_phones:
                        obj.messages.messages_to_send.insert(0, {'phone': phone['phone'], 'message': random.choice(obj.bots_messages), 'id': 0, 'image': None, 'buttons': None, 'title': None, 'footer': None, 'answer': None})
                    obj.logger.info('bots phones inserted')
                if obj.calls_enabled:
                    for phone in obj.call_phones:
                        obj.messages.messages_to_send.insert(0, {'phone': phone, 'message': 'звонок', 'id': 0, 'image': None, 'buttons': None, 'title': None, 'footer': None, 'answer': None})
                    obj.logger.info('call phones inserted')
                obj.d.press('back')
            elif obj.contacts_refresh_attempts > 10:
                obj.logger.error(f'contacts not synced!')
                raise core.exceptions.StopThreadException
            else:
                if obj.app == 'com.whatsapp':
                    obj.contacts_refresh_attempts += 1
                obj.d.press('back')
        else:
            obj.contacts_refreshed = True
            obj.d.press('back')


def handle_home(obj: script_iterator.ScriptIterator):
    # Херня, которая может вылезти попапом
    if obj.d(resourceId="com.whatsapp:id/design_bottom_sheet").exists:
        obj.d.keyevent('back')
    if obj.task == 'send' and obj.campaign.read_messages:
        utils.get_wa_answers(obj.d)
    # Хардкод настроек аккаунта
    if not obj.account.about and obj.app == 'com.whatsapp.w4b':
        obj.account.about = 'any'

    # --> В настройки аккаунта (handle_settings)
    if not obj.account.two_step_auth_code or (not obj.account.photo and obj.account.registered) or not obj.account.about or obj.change_name or obj.change_photo:
        obj.d(resourceId=f'{obj.app}:id/menuitem_overflow').click()
        obj.d(text='Settings').click()

    # --> В обновление контактов (handle_contacts)
    elif not obj.contacts_refreshed and obj.options.contacts.phones and obj.account.registered:
        display = utils.get_display(obj.d)
        if display.get('resource-id', f'{obj.app}:id/fab').exists:
            obj.d(resourceId=f"{obj.app}:id/fab").click()
        else:
            obj.d(resourceId=f"{obj.app}:id/fabText").click()

    # --> В создание веб-бекапа (handle_linked_devices)
    elif not obj.account.web_backup and obj.options.make_web_backup and not obj.failed_web:
        obj.d(resourceId=f'{obj.app}:id/menuitem_overflow').click()
        obj.d(text='Linked devices').click()

    else:
        # Создание мобильного бекапа
        # if not obj.account.backup:
        #     obj.logger.info(f'creating backup...')
        #     obj.account.backup = backup.create.create_dump(obj.serial, obj.app, obj.cdn)
        #     obj.d.shell(f'fallocate -l 1M {config.PHONE_TMP_FOLDER}/backup_{obj.account.backup}')
        #     obj.logger.info(f'backup created!')

        # Завершение реги
        if not obj.account.registered:
            obj.options.code_activator.phone_confirm(obj.account.activate_service_id)
            obj.account.registered = True

        # Качаем картинку
        if obj.messages.images and not obj.image_loaded:
            with Image.open(BytesIO(base64.b64decode(obj.messages.images[0].replace('data:image/jpeg;base64,', '')))) as image:
                image.save(f'{SAVE_IMG_PATH}/tmp_photo_{obj.account.id}.jpg')
            obj.d.push(f'{SAVE_IMG_PATH}/tmp_photo_{obj.account.id}.jpg', PHONE_IMAGES_FOLDER)
            obj.d.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{PHONE_IMAGES_FOLDER}/tmp_photo_{obj.account.id}.jpg')
            os.remove(f'{SAVE_IMG_PATH}/tmp_photo_{obj.account.id}.jpg')
            time.sleep(5)
            obj.image_loaded = True

        # --> В отправку (handle_conversation)
        if obj.messages.messages_to_send:
            if obj.group_sending and ((obj.calls_enabled and obj.calls_finished) or not obj.calls_enabled) and ((obj.bots_enable and obj.bots_finished) or not obj.bots_enable):
                if obj.calls_finished:
                    obj.calls_finished = None
                # Почему то на одних версиях могут по разному находиться кнопки
                if obj.d(description="Communities").exists:
                    obj.d(description="Communities").click()
                else:
                    if obj.d.xpath(f'//*[@resource-id="{obj.app}:id/top_navigation_tabs"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').exists:
                        obj.d.xpath(f'//*[@resource-id="{obj.app}:id/top_navigation_tabs"]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]').click()
                if obj.group_created:
                    if obj.d(resourceId=f"{obj.app}:id/conversations_row_contact_name", text=obj.group_name).exists:
                        obj.d(resourceId=f"{obj.app}:id/conversations_row_contact_name", text=obj.group_name).click()
                    else:
                        # Группа не успела создаться, фейкуем
                        obj.logger.info('Группа не прогрузилась')
                        time.sleep(5)
                        if obj.d(resourceId=f"{obj.app}:id/community_subject", text=obj.community_name).exists:
                            obj.d(resourceId=f"{obj.app}:id/community_subject", text=obj.community_name).click()
                        else:
                            obj.d(resourceId=f"{obj.app}:id/community_subject", text="New community").click()

                if obj.d.xpath(f'//*[@resource-id="{obj.app}:id/community_recycler_view"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]').exists:
                    obj.d.xpath(f'//*[@resource-id="{obj.app}:id/community_recycler_view"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]').click()
                else:
                    time.sleep(5)
                    obj.d(resourceId=f"{obj.app}:id/empty_community_row_button").click()
            else:
                if obj.campaign.without_internet:
                    phone_preparation.turn_airplane_mode(obj.d, on=True)
                if (obj.messages.messages_to_send[0]).get('image') is None:
                    obj.d.shell(f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' + obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + '" -p com.whatsapp')
                else:
                    obj.d.shell(f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' + obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + '" -p com.whatsapp' + f' --eu android.intent.extra.STREAM file:///{PHONE_IMAGES_FOLDER}/tmp_photo_{obj.account.id}.jpg')

        else:
            if obj.campaign.without_internet:
                phone_preparation.turn_airplane_mode(obj.d, on=False)
                future = datetime.now() + timedelta(seconds=obj.campaign.parameters['without_internet_timeout'])
                not_sent = len(list(filter(lambda s: s == 'not sent', utils.get_wa_messages(obj.d, True).values())))
                while not_sent > 0:
                    tmp_not_sent = len(list(filter(lambda s: s == 'not sent', utils.get_wa_messages(obj.d, True).values())))
                    if tmp_not_sent != not_sent:
                        not_sent = tmp_not_sent
                        future = datetime.now() + timedelta(seconds=obj.campaign.parameters['without_internet_timeout'])
                    if datetime.now() >= future:
                        obj.logger.warning(f'timeout on sending messages!')
                        break
                    time.sleep(2)
            obj.logger.info(f'end of script reached!')
            if obj.campaign.read_messages and obj.task == 'send':
                utils.get_wa_answers(obj.d)
            if not obj.account.backup and obj.task == 'reg' and obj.account.registered:
                obj.d.press('home')
            else:
                raise core.exceptions.StopThreadException


def handle_linked_devices(obj: script_iterator.ScriptIterator):
    if obj.failed_web:
        obj.d.press('back')
    elif obj.backup_service:
        timer = 0
        while not obj.backup_service.check_backup_exists() and timer < 60:
            time.sleep(1)
            timer += 1
        obj.backup_service.finish()
        if obj.backup_service.check_backup_exists():
            obj.account.web_backup = obj.account.backup
        obj.d.press('back')
    else:
        display = utils.get_display(obj.d)
        if display.get('resource-id', f'{obj.app}:id/name').exists:
            # сделать обработку удаления имеющихся коннектов
            if obj.app == 'com.whatsapp.w4b':
                obj.d(resourceId=f"{obj.app}:id/primary_button").click()
            else:
                obj.d(resourceId=f"{obj.app}:id/name").click()
        else:
            obj.d(resourceId=f"{obj.app}:id/link_device_button").click()


def handle_pair_web(obj: script_iterator.ScriptIterator):
    try:
        if not obj.backup_service:
            obj.backup_service = BackupService(obj.serial, obj.account.backup, config.DEVICE_PAIRS)
            obj.backup_service.delete_web_backup()
            obj.backup_service.create_web_backup()
            display = utils.get_display(obj.d)
            if display.get('resource-id', f'{obj.app}:id/education').exists:
                obj.d(resourceId=f"{obj.app}:id/ok").click()
    except BackupServiceException as e:
        if not isinstance(e, BackupExistsException):
            obj.backup_service = None
            obj.logger.warning(f'web backup service exception!')
        # obj.failed_web = True
        obj.d.press('back')


def handle_web_logout(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/logout_text").click()


def handle_connect_wifi(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_web_check_internet(obj: script_iterator.ScriptIterator):
    obj.backup_service = None
    obj.d(resourceId="android:id/button1").click()


def handle_new_web(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_couldnt_link(obj: script_iterator.ScriptIterator):
    obj.backup_service.finish()
    obj.backup_service = None
    obj.d(resourceId="android:id/button1").click()


def handle_not_valid(obj: script_iterator.ScriptIterator):
    # obj.messages.messages_not_valid.append(obj.messages.messages_to_send.pop(0))
    obj.d(resourceId='android:id/button1').click()


def handle_couldnt_find_phone(obj: script_iterator.ScriptIterator):
    obj.d.press('back')


def handle_conversation(obj: script_iterator.ScriptIterator):
    if obj.just_sent_image is True and not obj.group_participants_inserted:
        obj.just_sent_image = False
        obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
        obj.last_sent = datetime.now()

        if obj.messages.messages_to_send:
            if (obj.messages.messages_to_send[0]).get('image') is None:
                obj.d.shell(f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' + obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + f'" -p {obj.app}')
            else:
                obj.d.shell(f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' + obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + f'" -p {obj.app}' + f' --eu android.intent.extra.STREAM file:///{PHONE_IMAGES_FOLDER}/tmp_photo_{obj.account.id}.jpg')
                time.sleep(1)

    if obj.calls_enabled and len(obj.messages.messages_sent) < obj.call_times:
        _call_warmup(obj)

    if obj.bots_enable and len(obj.messages.messages_sent) < obj.bots_amount:
        _bot_warmup(obj)

    if obj.group_sending:
        # После прогревов выходим из переписки
        if not obj.group_community_set_name and (obj.calls_finished or obj.bots_finished):
            if obj.conversation_exists > 0:
                obj.d(resourceId=f"{obj.app}:id/conversation_contact").click()
            else:
                obj.conversation_exists += 1
                obj.d.keyevent('back')
        # Обработка попапа
        if obj.d(resourceId=f"{obj.app}:id/bottom_sheet_close_button").exists:
            obj.d(resourceId=f"{obj.app}:id/bottom_sheet_close_button").click()
        if obj.group_with_image and not obj.group_community_set_photo:
            obj.d(resourceId=f"{obj.app}:id/conversation_contact").click()
        if obj.group_participants_inserted:
            # Фикс бесконечного цикла с картинками
            if obj.just_sent_image:
                obj.logger.info('just sent image')
                obj.messages.messages_sent = obj.messages.messages_to_send[:]
                obj.messages.messages_to_send.clear()
                time.sleep(6)
                raise core.exceptions.StopThreadException

            if obj.group_community_sending:
                obj.logger.info(f"before text setting {obj.group_message.format(uniq_id=obj.messages.messages_to_send[-1]['message'].split('/')[-1])}")
                obj.d(resourceId=f"{obj.app}:id/entry").set_text(obj.group_message.format(uniq_id=obj.messages.messages_to_send[-1]['message'].split('/')[-1]))
            else:
                # В кампании: Переходи по ссылке: get2bonus.ru/{uniq_id} ...
                obj.d(resourceId=f"{obj.app}:id/entry").set_text(obj.group_message.format(uniq_id=obj.group_chunked_messages[0][1]))
            # Прикрепление картинки
            if obj.group_sending_with_image:
                obj.logger.info('before sending image downloading')
                utils.GroupImage.upload(device=obj.d, image=obj.sending_image)
                obj.logger.info('Downloading image to sending')
                obj.d(resourceId=f"{obj.app}:id/input_attach_button").click()

            obj.d(resourceId=f"{obj.app}:id/conversation_entry_action_button").click()

            if obj.chunks_enabled:
                # Вставка уникальных значений, чтобы потом отследить их в базе ватсапа
                obj.group_message_sent[obj.group_chunked_messages[0][1]] = obj.group_chunked_messages[0][0]

                popped_messages = obj.group_chunked_messages.pop(0)
                obj.messages.messages_to_send = list(filter(lambda x: x not in popped_messages[0], obj.messages.messages_to_send))
                obj.messages.messages_sent.extend(popped_messages[0])
            else:
                obj.messages.messages_sent = obj.messages.messages_to_send[:]
                obj.messages.messages_to_send.clear()

            # Ждем, чтобы смс отправилась (интернет)
            time.sleep(6)

            if obj.chunks_enabled and obj.group_chunked_messages:
                # Обнуляем все флаги
                obj.group_set_name = False
                obj.group_participants_inserted = False
                obj.group_set_photo = False
                obj.group_created = False
                obj.group_permission_set = False

                obj.d.keyevent('back')
                obj.d.keyevent('back')
            else:
                raise core.exceptions.StopThreadException

        obj.d(resourceId=f"{obj.app}:id/conversation_contact").click()
        return
    else:
        while obj.messages.messages_to_send:
            if obj.without_internet_w_warm and ((obj.bots_enable and len(obj.messages.messages_sent) >= obj.bots_amount) or (obj.calls_enabled and len(obj.messages.messages_sent) >= obj.call_times or obj.first_calls_enabled)) and not obj.campaign.without_internet:
                phone_preparation.turn_airplane_mode(obj.d, on=True)
                obj.campaign.without_internet = True
                obj.device_info.params['without_internet'] = True
            find_to = datetime.now() + timedelta(seconds=1)
            display = utils.get_display(obj.d)
            phone = utils.normalize_phone(display.get('resource-id', f'{obj.app}:id/conversation_contact_name').text)

            while datetime.now() < find_to and (obj.messages.messages_to_send[0]['phone'] != phone or display.get('resource-id', f'{obj.app}:id/entry').text == 'Message'):
                display = utils.get_display(obj.d)
                phone = utils.normalize_phone(display.get('resource-id', f'{obj.app}:id/conversation_contact_name').text)

            # if display.get('resource-id', f'{obj.app}:id/entry').text != 'Message':
            if obj.messages.messages_to_send[0]['phone'] == phone and display.get('resource-id', f'{obj.app}:id/entry').text != 'Message':
                if obj.last_sent:
                    if obj.bots_enable and obj.bots_pause_enable and len(obj.messages.messages_sent) < obj.bots_amount:
                        sleep_to = obj.last_sent + timedelta(seconds=(obj.bots_breaktime_min + random.randint(0, obj.bots_breaktime_rand)))
                    else:
                        sleep_to = obj.last_sent + timedelta(seconds=(obj.options.messages_breaktime_min + random.randint(0, obj.options.messages_breaktime_rand)))
                    while datetime.now() < sleep_to:
                        if obj.campaign.read_messages:
                            obj.messages.messages_income = utils.get_wa_answers(obj.d)
                        time.sleep(1)
                try:
                    obj.d(resourceId=f'{obj.app}:id/send_container').click()
                    obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
                    obj.last_sent = datetime.now()
                except UiObjectNotFoundError:
                    obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_ok').click()
                    obj.d(resourceId=f'{obj.app}:id/send_container').click()
                    obj.messages.messages_sent.append(obj.messages.messages_to_send.pop(0))
                    obj.last_sent = datetime.now()

            elif display.get('resource-id', f'{obj.app}:id/ephemeral_nux_ok').text == 'OK':
                obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_ok').click()

            if obj.campaign.parameters['timeout_after_send']:
                time.sleep(obj.campaign.parameters['timeout_after_send'])

            if obj.messages.messages_to_send:
                if (obj.messages.messages_to_send[0]).get('image') is None:
                    obj.d.shell(f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' + obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + f'" -p {obj.app}')
                else:
                    obj.d.shell(f'am start -a android.intent.action.SEND -c android.intent.category.DEFAULT -t text/plain -e jid ' + obj.messages.messages_to_send[0]['phone'] + '@s.whatsapp.net -e android.intent.extra.TEXT "' + (obj.messages.messages_to_send[0]['message']).replace('"', '\\"') + f'" -p {obj.app}' + f' --eu android.intent.extra.STREAM file:///{PHONE_IMAGES_FOLDER}/tmp_photo_{obj.account.id}.jpg')
                    time.sleep(1)

    obj.d.keyevent('back')


def handle_attachments(obj: script_iterator.ScriptIterator):
    if obj.group_sending_with_image:
        obj.d(resourceId=f"{obj.app}:id/pickfiletype_gallery_holder")
    else:
        # нельзя ставить фотку в мобайле
        obj.d.keyevent('back')


def handle_send_attachments(obj: script_iterator.ScriptIterator):
    if obj.last_sent:
        sleep_to = obj.last_sent + timedelta(seconds=(obj.options.messages_breaktime_min + random.randint(0, obj.options.messages_breaktime_rand)))
        while datetime.now() < sleep_to:
            time.sleep(1)
    obj.last_sent = datetime.now()

    obj.just_sent_image = True
    obj.d(resourceId=f'{obj.app}:id/send').click()


def handle_call(obj: script_iterator.ScriptIterator):
    obj.logger.info('start call')
    find_to = datetime.now() + timedelta(seconds=5)
    while datetime.now() < find_to:
        display = utils.get_display(obj.d)
        mute_btn_check = display.get('resource-id', f'{obj.app}:id/mute_btn')
        if mute_btn_check.exists:
            if obj.d(resourceId=f"{obj.app}:id/mute_btn").info.get('contentDescription') == 'Mute microphone':
                obj.d(resourceId=f"{obj.app}:id/mute_btn").click()
            break
    else:
        obj.logger.info('cant found mute_btn')


    timeout = datetime.now() + timedelta(seconds=obj.to_call_timeout_seconds)
    is_call_accepted = False
    while datetime.now() < timeout:
        display = utils.get_display(obj.d)
        call_status_check = display.get('resource-id', f'{obj.app}:id/call_status')
        is_call_enable = display.get('resource-id', f'{obj.app}:id/toggle_video_btn')

        # проверка сбросили или недозвон или входящий
        if call_status_check.text == 'Call declined':
            obj.messages.messages_sent[-1]['message'] = 'declined'
            obj.logger.info('Call declined')
            obj.d(resourceId=f"{obj.app}:id/cancel_call_back_btn").click()
            break
        elif call_status_check.text == "Didn't answer":
            obj.messages.messages_sent[-1]['message'] = 'no_answer'
            obj.logger.info("Didn't answer")
            obj.d(resourceId=f"{obj.app}:id/cancel_call_back_btn").click()
            break
        elif call_status_check.text == "WhatsApp voice call":
            obj.logger.info("Incoming call")
            obj.d(resourceId=f"{obj.app}:id/decline_incoming_call_view").drag_to()
            obj.had_incoming_call = True
            break

        # проверка дозвона
        enabled = is_call_enable.attributes.get('enabled')
        if enabled == 'true':
            obj.messages.messages_sent[-1]['message'] = 'accepted'
            obj.logger.info("Call accepted")
            if not is_call_accepted:
                is_call_accepted = True
                timeout = datetime.now() + timedelta(seconds=obj.talking_timeout_seconds)

            # obj.d(resourceId=f"{obj.app}:id/footer_end_call_btn").click()
            # obj.d(resourceId="android:id/button2").click()
            # break
        obj.logger.info('checking call')
        time.sleep(1)
    else:
        obj.logger.info("Timeout talking" if is_call_accepted else "Timeout call")
        if not is_call_accepted:
            obj.messages.messages_sent[-1]['message'] = 'no_answer'
        obj.d(resourceId=f"{obj.app}:id/footer_end_call_btn").click()
        if is_call_accepted:
            obj.d(resourceId="android:id/button2").click()


def accept_call_start(obj: script_iterator.ScriptIterator):
    obj.logger.info('trying make call')
    # клик возможно мажет и скрывает попап
    if obj.d(resourceId='android:id/button1').exists:
        obj.d(resourceId='android:id/button1').click()

    time.sleep(5)


def handle_delete_chat(obj: script_iterator.ScriptIterator):
    obj.d(resourceId='android:id/button1').click()


def handle_smb_requested_code(obj: script_iterator.ScriptIterator):
    obj.d(resourceId='android:id/button1').click()


def handle_settings(obj: script_iterator.ScriptIterator):
    if (not obj.account.photo and obj.account.registered) or obj.change_photo:
        obj.d(resourceId=f'{obj.app}:id/profile_info').click()
    elif not obj.account.about:
        obj.d(resourceId=f'{obj.app}:id/profile_info').click()
    elif not obj.account.two_step_auth_code:
        obj.d(resourceId=f'{obj.app}:id/settings_account_info').click()
    elif not obj.account.name or obj.change_name:
        obj.d(resourceId=f'{obj.app}:id/profile_info').click()
    else:
        obj.d.keyevent('back')


def import_contacts(obj: script_iterator.ScriptIterator):
    obj.d.xpath('//*[@resource-id="com.samsung.android.app.contacts:id/menu_done"]/android.view.ViewGroup[1]').click()


def handle_profile_settings(obj: script_iterator.ScriptIterator):
    if (not obj.account.photo and obj.account.registered) or obj.change_photo:
        photos.photos_manager.remove_all_photos(obj.d)
        if obj.client == 'skillbox':
            obj.account.photo = photos.photos_manager.get_and_save_skillbox_on_photo(obj.d)
        elif obj.options.data_for_account:
            obj.account.photo = photos.photos_manager.get_and_save_generated_photo(obj.d, obj.options.data_for_account.photo_url)
        else:
            obj.account.photo = photos.photos_manager.get_and_save_random_on_photo(obj.d)
        obj.change_photo = False
        time.sleep(5)
        obj.d(resourceId=f'{obj.app}:id/change_photo_btn').click()
        obj.d(resourceId=f"{obj.app}:id/name", text="Gallery").click()
    elif not obj.account.about:
        obj.d(resourceId=f'{obj.app}:id/profile_info_status_card').click()
    elif not obj.account.name or obj.change_name:
        if obj.options.data_for_account:
            name = obj.options.data_for_account.name
        else:
            name = utils.gen_name()
        obj.account.name = name
        obj.change_name = False
        obj.d(resourceId=f"{obj.app}:id/profile_settings_row_secondary_icon").click()
        time.sleep(1)
        obj.d(resourceId=f"{obj.app}:id/edit_text").set_text(name)
        time.sleep(1)
        obj.d(resourceId=f"{obj.app}:id/save_button").click()
        obj.d.keyevent("back")
    else:
        obj.d.keyevent('back')


def handle_profile_settings_b(obj: script_iterator.ScriptIterator):
    if (not obj.account.photo and obj.account.registered) or obj.change_photo:
        photos.photos_manager.remove_all_photos(obj.d)
        if obj.client == 'skillbox':
            obj.account.photo = photos.photos_manager.get_and_save_skillbox_on_photo(obj.d)
        elif obj.options.data_for_account:
            obj.account.photo = photos.photos_manager.get_and_save_generated_photo(obj.d, obj.options.data_for_account.photo_url)
        else:
            obj.account.photo = photos.photos_manager.get_and_save_random_on_photo(obj.d)
        obj.change_photo = False
        time.sleep(5)
        obj.d(resourceId=f'{obj.app}:id/profile_picture_image').click()
        obj.d(resourceId=f"{obj.app}:id/name", text="Gallery").click()
    elif not obj.account.name or obj.change_name:
        obj.d(resourceId=f"{obj.app}:id/form_field_edit_icon").click()
    else:
        time.sleep(2)
        obj.d.keyevent('back')


def handle_edit_name(obj: script_iterator.ScriptIterator):
    if obj.options.data_for_account:
        name = obj.options.data_for_account.name
    else:
        name = utils.gen_name()
    obj.d(resourceId=f"{obj.app}:id/edit_text").set_text(name)
    obj.d(resourceId=f"{obj.app}:id/ok_btn").click()
    obj.d(resourceId=f"android:id/button1").click()
    obj.d(resourceId=f"android:id/button1").click()
    obj.account.name = name
    obj.change_name = False
    obj.d.keyevent("back")


def handle_about(obj: script_iterator.ScriptIterator):
    if not obj.account.about or not utils.get_display(obj.d).get('resource-id', f'{obj.app}:id/status_tv').text == obj.account.about:
        set_status = random.choice(['Available', 'Busy', 'At school', 'At work', 'Sleeping', 'In a meeting', 'Battery about to die', 'Can\'t talk, WhatsApp only'])
        obj.account.about = set_status
        obj.d(resourceId=f"{obj.app}:id/status_row", text=set_status).click()
        time.sleep(1)
    obj.d.keyevent('back')


def handle_choose_album(obj: script_iterator.ScriptIterator):
    # Вставка фото в комюнити/группы
    if obj.group_sending:
        obj.d(resourceId=f"{obj.app}:id/title").click()

    if obj.app == 'com.whatsapp.w4b':
        time.sleep(3)
    time.sleep(0.5)
    display = utils.get_display(obj.d)
    if display.get('text', 'Camera photos').exists:
        obj.d(resourceId=f"{obj.app}:id/title", text="Camera photos").click()
    elif display.get('text', 'Camera').exists:
        obj.d(resourceId=f"{obj.app}:id/title", text="Camera").click()
    elif display.get('text', 'All photos').exists:
        obj.d(resourceId=f"{obj.app}:id/title", text="All photos").click()
    elif obj.d.xpath(f'//*[@resource-id="{obj.app}:id/grid"]/android.widget.ImageView[1]').exists:
        obj.d.xpath(f'//*[@resource-id="{obj.app}p:id/grid"]/android.widget.ImageView[1]').click()
    else:
        obj.account.photo = None
        obj.logger.error('cant set photo, no album!')
        raise core.exceptions.StopThreadException
    if obj.app == 'com.whatsapp.w4b':
        time.sleep(2)


def handle_set_name_b(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/device_name_edit_text").set_text(obj.account.name)
    obj.d(resourceId=f"{obj.app}:id/save_device_name_btn").click()


def handle_choose_photo(obj: script_iterator.ScriptIterator):
    time.sleep(0.5)
    display = utils.get_display(obj.d)
    if display.get('content-desc', 'Photo').exists:
        obj.d(description="Photo").click()
    else:
        obj.account.photo = None
        raise core.exceptions.StopThreadException
    time.sleep(1)


def handle_photo_crop(obj: script_iterator.ScriptIterator):
    if obj.group_sending:
        if obj.group_community_set_photo and not obj.group_set_photo:
            obj.group_set_photo = True
        if not obj.group_community_set_photo:
            obj.group_community_set_photo = True
    obj.d(resourceId=f"{obj.app}:id/ok_btn").click()


def handle_account_settings(obj: script_iterator.ScriptIterator):
    if not obj.account.two_step_auth_code:
        obj.d(resourceId=f'{obj.app}:id/two_step_verification_preference').click()
    else:
        obj.d.keyevent('back')


def handle_twofactor_settings(obj: script_iterator.ScriptIterator):
    if not obj.account.two_step_auth_code:
        obj.d(resourceId=f'{obj.app}:id/enable_button').click()
    else:
        obj.d.keyevent('back')


def handle_twofactor_settings_inner(obj: script_iterator.ScriptIterator):
    if not obj.account.two_step_auth_code:
        code = f'{random.randint(0, 999_999):06d}'
        obj.d(resourceId=f'{obj.app}:id/code').set_text(code)
        obj.d(resourceId=f'{obj.app}:id/code').set_text(code)
        obj.d(resourceId=f'{obj.app}:id/email').set_text(f'{code}@gmail.com')
        obj.d(resourceId=f'{obj.app}:id/submit').click()
        obj.d(resourceId=f'{obj.app}:id/email').set_text(f'{code}@gmail.com')
        obj.account.two_step_auth_code = code
        obj.d(resourceId=f'{obj.app}:id/submit').click()
        time.sleep(3)
    if utils.get_display(obj.d).get('resource-id', f'{obj.app}:id/done_button').exists:
        obj.d(resourceId=f'{obj.app}:id/done_button').click()
    else:
        obj.d.keyevent('back')


def enter_pin(obj: script_iterator.ScriptIterator):
    try:
        obj.d(resourceId=f'{obj.app}:id/code').set_text(obj.account.two_step_auth_code)
    except UiObjectNotFoundError:
        ...


def skip_new(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f'{obj.app}:id/ephemeral_nux_finished').click()


def disagree_popup(obj: script_iterator.ScriptIterator):
    obj.d(resourceId='android:id/button2').click()


def handle_google_drive(obj: script_iterator.ScriptIterator):
    time.sleep(2)
    obj.d(text="Never").click()
    obj.d(resourceId=f"{obj.app}:id/gdrive_new_user_setup_btn").click()


def handle_link_fb(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_viewer_photo(obj: script_iterator.ScriptIterator):
    obj.change_photo = False
    obj.d.press('back')


def handle_samsung_contacts(obj: script_iterator.ScriptIterator):
    obj.d.press('back')


def handle_loading_backup(obj: script_iterator.ScriptIterator):
    time.sleep(5)


def handle_drony(obj: script_iterator.ScriptIterator):
    # ждем пока вылезет ".ConfirmDialog" -> handle_drony_icon
    time.sleep(2)
    # ставим прокси в базе drony
    set_proxy(obj.d, obj.proxy.host, obj.proxy.port, obj.proxy.username, obj.proxy.password, obj.proxy.type)
    # ждем пока дрони подхватит изменения
    time.sleep(2)
    display = utils.get_display(obj.d)
    description = display.get('resource-id', f'org.sandroproxy.drony:id/toggleButtonOnOff')
    if description.text == 'OFF':
        obj.d(resourceId="org.sandroproxy.drony:id/toggleButtonOnOff").click()
        time.sleep(2)
    else:
        obj.d(resourceId="org.sandroproxy.drony:id/toggleButtonOnOff").click()
        time.sleep(1)
        obj.d(resourceId="org.sandroproxy.drony:id/toggleButtonOnOff").click()
    obj.proxy_ready, obj.proxy.change = True, False
    obj.d.press('home')


# пермишены выдаются через adb, но окошко все равно появляется
def handle_drony_permission(obj: script_iterator.ScriptIterator):
    obj.d.press('back')
    time.sleep(2)


# надо разрешить показывать статус drony в трее
def handle_drony_icon(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()
    time.sleep(2)


def handle_try_again(obj: script_iterator.ScriptIterator):
    obj.proxy_ready = False
    if obj.proxy:
        obj.proxy.change = True
    obj.d.press('home')


def handle_captcha(obj: script_iterator.ScriptIterator):
    obj.logger.error('captcha occured, finish')
    raise core.exceptions.StopThreadException


def handle_decline(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button2").click()


def handle_spam_call(obj: script_iterator.ScriptIterator):
    obj.d(text="OK").click()


def handle_call_rating(obj: script_iterator.ScriptIterator):
    obj.d.press('back')


def handle_is_correct_number(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def end_whatsapp_call(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_popup_ok(obj: script_iterator.ScriptIterator):
    obj.device_info.params['connect_issue_during_call'] = True
    obj.d(resourceId="android:id/button1").click()


def handle_create_community(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/community_nux_next_button").click()


def handle_community_settings(obj: script_iterator.ScriptIterator):
    if obj.group_created:
        time.sleep(5)
        obj.d.keyevent('back')
    obj.d.xpath(f'//*[@resource-id="{obj.app}:id/name_text_container"]/android.widget.LinearLayout[1]').set_text(obj.community_name)
    if obj.community_with_image and not obj.invalid_photo:
        if not obj.group_community_set_photo:
            obj.group_community_set_name = True
            # Вставка картинки
            utils.GroupImage.upload(device=obj.d, image=obj.community_image)
            obj.logger.info('Downloading image to community setting')

            obj.d(resourceId=f"{obj.app}:id/new_community_change_photo").click()
            obj.d(resourceId=f"{obj.app}:id/name", text="Gallery").click()
        else:
            obj.d(resourceId=f"{obj.app}:id/new_community_next_button").click()
    else:
        obj.group_community_set_name = True
        obj.d(resourceId=f"{obj.app}:id/new_community_next_button").click()


def handle_add_new_group(obj: script_iterator.ScriptIterator):
    if not obj.group_community_set_name:
        obj.d.xpath(f'//*[@resource-id="{obj.app}:id/community_navigation_subgroup_recycler_view"]/android.widget.RelativeLayout[1]').click()
    if not obj.group_community_sending:
        obj.d(resourceId=f"{obj.app}:id/community_navigation_add_group_button").click()
    time.sleep(2)
    obj.d(resourceId=f"{obj.app}:id/contact_row_container").click()


def handle_create_new_group(obj: script_iterator.ScriptIterator):
    # if obj.group_set_name:
    #     obj.d(resourceId=f"{obj.app}:id/community_add_groups_done_button").click()
    # else:
    obj.d(text="Create new group").click()

    obj.group_created = True


def handle_set_name_group(obj: script_iterator.ScriptIterator):
    # if obj.group_participants_inserted:
    #     obj.d(resourceId=f"{obj.app}:id/ok_btn").click()
    time.sleep(1)
    if not obj.group_set_name:
        utils.generate_name_by_pattern(obj, to_community=False)
        obj.d.xpath(
            f'//*[@resource-id="{obj.app}:id/group_setting_layout"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[2]/android.widget.RelativeLayout[1]').set_text(
            obj.group_name)
        obj.group_set_name = True
        if obj.group_with_image and not obj.group_set_photo:
            utils.GroupImage.upload(device=obj.d, image=obj.group_image)
            obj.d(resourceId=f"{obj.app}:id/change_photo_btn").click()
            obj.d(resourceId=f"{obj.app}:id/name", text="Gallery").click()
        else:
            if obj.d(resourceId=f"{obj.app}:id/group_permissions_row_view").exists:
                obj.d(resourceId=f"{obj.app}:id/group_permissions_row_view").click()

        obj.d(resourceId=f"{obj.app}:id/ok_btn").click()
    else:
        obj.d(resourceId=f"{obj.app}:id/ok_btn").click()


def handle_add_partiсipants(obj: script_iterator.ScriptIterator):
    time.sleep(2)
    if obj.group_participants_inserted:
        obj.d.keyevent('back')
    if obj.group_permission_set:
        obj.d.swipe_ext("down", 0.99)
        obj.d(resourceId=f"{obj.app}:id/action_add_person").click()
    else:
        obj.d.swipe_ext("up", 0.99)
        obj.d(resourceId=f"{obj.app}:id/list_item_title", text="Group permissions").click()
        time.sleep(2)


def handle_participants_add(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()
    obj.d(resourceId=f"{obj.app}:id/next_btn").click()


def handle_special_participants(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()
    obj.d.keyevent('back')


def handle_choosing_participants(obj: script_iterator.ScriptIterator):
    if obj.group_participants_inserted:
        obj.d.keyevent('back')
        return
    obj.logger.info('Идет выбор контактов для группы')
    obj.d(resourceId=f"{obj.app}:id/menuitem_search").click()
    if obj.chunks_enabled:
        phones = [message['phone'] for message in obj.group_chunked_messages[0][0]]
    else:
        phones = [message['phone'] for message in obj.messages.messages_to_send if message['id'] != 0]
    for phone in phones:
        obj.d(resourceId=f"{obj.app}:id/search_src_text").set_text(phone)
        if obj.d(resourceId=f"{obj.app}:id/chat_able_contacts_row_name", text=f'+{phone}').exists:
            obj.d(resourceId=f"{obj.app}:id/chat_able_contacts_row_name", text=f'+{phone}').click()
        time.sleep(1)

    obj.d(resourceId=f"{obj.app}:id/next_btn").click()
    obj.group_participants_inserted = True
    obj.d.sleep(1)
    obj.d(resourceId="android:id/button1").click()


def handle_participants_cant_added(obj: script_iterator.ScriptIterator):
    time.sleep(1)
    if obj.d(resourceId=f"{obj.app}:id/bottom_sheet_close_button").exists:
        obj.d(resourceId=f"{obj.app}:id/bottom_sheet_close_button").click()
    if obj.group_created:
        time.sleep(5)
        obj.d.keyevent('back')
    elif obj.d(resourceId="android:id/button1").exists:
        obj.d(resourceId="android:id/button1").click()
    if not obj.group_set_name and not obj.group_community_set_name:
        obj.d.swipe_ext("up", 0.99)
        if obj.d(resourceId=f"{obj.app}:id/list_item_title", text="Deactivate community").exists:
            obj.d(resourceId=f"{obj.app}:id/list_item_title", text="Deactivate community").click()
        else:
            obj.d(description="Community").click()
            time.sleep(1)

            # 6 попыток, если кнопку не находит, то значит не наше комьюнити, следовательно выходим
            attempts = 0
            while not obj.d(resourceId=f"{obj.app}:id/list_item_title", text="Deactivate community").exists:
                if attempts == 6:
                    break
                obj.d.swipe_ext("up", 0.99)
                time.sleep(1)
                attempts += 1
            if attempts == 5:
                obj.strange_community = True
                obj.d(resourceId=f"{obj.app}:id/list_item_title", text="Exit community").click()
            else:
                obj.d(resourceId=f"{obj.app}:id/list_item_title", text="Deactivate community").click()

    elif obj.group_community_sending and not obj.group_participants_inserted:
        obj.d(resourceId=f"{obj.app}:id/action_add_members").click()
    else:
        obj.d.keyevent('back')


def handle_participants_community_add(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_participants_cant_added_phones(obj: script_iterator.ScriptIterator):
    if utils.get_display(obj.d).get(key='text', value="You can't add participants because you're not a participant.").exists:
        handle_ban(obj)
    if obj.d(resourceId="android:id/button2").exists:
        obj.d(resourceId="android:id/button2").click()
    else:
        obj.d.keyevent('back')


def handle_group_permissions(obj: script_iterator.ScriptIterator):
    obj.group_set_name = True
    obj.group_permission_set = True
    obj.d.xpath(f'//*[@resource-id="{obj.app}:id/restricted_mode_layout"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]').click()
    time.sleep(1)
    obj.d.xpath(f'//*[@resource-id="{obj.app}:id/announcement_group_layout"]/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]').click()
    obj.d.keyevent('back')


def handle_deactivate_community(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/community_deactivate_disclaimer_continue_button").click()


def handle_deactivate_community_popup(obj: script_iterator.ScriptIterator):
    obj.d(resourceId="android:id/button1").click()


def handle_choosing_attachment(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/pickfiletype_gallery_holder").click()


def handle_contact_info(obj: script_iterator.ScriptIterator):
    if obj.call_times:
        if len(obj.messages.messages_sent) >= obj.call_times:
            obj.calls_finished = True
    obj.d.keyevent('back')


def handle_community_home_popups(obj: script_iterator.ScriptIterator):
    if obj.d(resourceId="android:id/button2").exists:
        obj.d(resourceId="android:id/button2").click()
    elif utils.get_display(obj.d).get(key='text', value="You can't add participants because you're not a participant.").exists:
        handle_ban(obj)
    elif obj.strange_community:
        obj.d(resourceId="android:id/button1").click()
    elif utils.get_display(obj.d).get(key='text', value="Adding...").exists:
        obj.d.keyevent('back')


def handle_voip_activity(obj: script_iterator.ScriptIterator):
    # Как я понял, аналогично .Conversation
    if obj.d(resourceId=f"{obj.app}:id/conversation_contact").exists:
        obj.d(resourceId=f"{obj.app}:id/conversation_contact").click()
    else:
        obj.d.keyevent('back')


def handle_participants_not_now(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/btn_not_now").click()


def handle_bad_resolution(obj: script_iterator.ScriptIterator):
    # невалидное разрешение картинки
    if obj.d(resourceId="android:id/message").exists:
        obj.invalid_photo = True
        obj.d(resourceId="android:id/button1").click()


def handle_register_email(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/register_email_skip").click()


def handle_conversation_airmode(obj: script_iterator.ScriptIterator):
    phone_preparation.turn_airplane_mode(obj.d, on=False)
    obj.d.keyevent('back')


def handle_group_image_sending(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/text", text="Gallery").click()


def handle_group_image_choose(obj: script_iterator.ScriptIterator):
    if obj.d.xpath(f'//*[@resource-id="{obj.app}:id/albums"]/android.widget.FrameLayout[1]').exists:
        obj.d.xpath(f'//*[@resource-id="{obj.app}:id/albums"]/android.widget.FrameLayout[1]').click()


def handle_go_back(obj: script_iterator.ScriptIterator):
    obj.d.keyevent('back')


def handle_click_registration_submit(obj: script_iterator.ScriptIterator):
    obj.d(resourceId=f"{obj.app}:id/registration_submit").click()


def handle_send_sms(obj: script_iterator.ScriptIterator):
    if obj.d(text="SEND SMS").exists:
        obj.d(text="SEND SMS").click()


def handle_create_community_or_nothing(obj: script_iterator.ScriptIterator):
    if obj.d(resourceId=f"{obj.app}:id/community_nux_next_button").exists:
        obj.d(resourceId=f"{obj.app}:id/community_nux_next_button").click()


def handle_set_text_or_nothing(obj: script_iterator.ScriptIterator):
    try:
        handle_community_settings(obj)
    except:
        ...


def handle_conversation_popup(obj: script_iterator.ScriptIterator):
    if utils.get_display(obj.d).get(key='text', value="Couldn\'t place call. Make sure your device has an Internet connection and try again.").exists:
        handle_popup_ok(obj)
    elif utils.get_display(obj.d).get(key='text', value="To place a WhatsApp call, first turn off Airplane mode.").exists:
        handle_conversation_airmode(obj)
    elif utils.get_display(obj.d).get(key='text', value='Document').exists:
        handle_attachments(obj)
    elif utils.get_display(obj.d).get(key='text', value="just answered your call. Do you want to continue the call?").exists:
        handle_decline(obj)
    else:
        if obj.d(resourceId=f"{obj.app}:id/conversation_entry_action_button").exists:
            obj.d(resourceId=f"{obj.app}:id/conversation_entry_action_button").click()
        else:
            handle_go_back(obj)


def handle_register_email_or_back(obj: script_iterator.ScriptIterator):
    if obj.d(resourceId=f"{obj.app}:id/register_email_skip").exists:
        obj.d(resourceId=f"{obj.app}:id/register_email_skip").click()
    else:
        obj.d.keyevent('back')


def handle_google_drive_or_back(obj: script_iterator.ScriptIterator):
    try:
        time.sleep(2)
        obj.d(text="Never").click()
        obj.d(resourceId=f"{obj.app}:id/gdrive_new_user_setup_btn").click()
    except:
        obj.d.keyevent('back')


def enter_reg_phone_or_back(obj: script_iterator.ScriptIterator):
    try:
        enter_reg_phone(obj)
    except:
        obj.d.keyevent('back')


def handle_stop_iteration(obj: script_iterator.ScriptIterator):
    obj.logger.error(f'handle_stop_iteration {obj.current_activity}')
    raise core.exceptions.StopThreadException


def handle_add_new_group_or_back(obj: script_iterator.ScriptIterator):
    try:
        handle_add_new_group(obj)
    except:
        obj.d.keyevent('back')


def skip_email(obj: script_iterator.ScriptIterator):
    time.sleep(1)
    obj.d(text='SKIP').click()
