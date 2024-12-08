import concurrent.futures
import os
import random
import re
import subprocess
import time
from typing import Iterable, Sequence
from unicodedata import normalize
import uuid
import requests

from mimesis import Person, locales, enums
import sentry_sdk
import uiautomator2 as u2

import config
from core.app_page_parser import AppPageFabric
from datetime import datetime

import functools

from services.cdn.selectel import SelectelCDN


sentry_sdk.init(dsn="https://a32fb9b2252544609dbe4f6d882825f4@sentry.caltat.com/5")


def get_display(device):
    return AppPageFabric.str_to_element(device.dump_hierarchy())


def app_current(d):
    for i in range(10):
        package = None
        ret = None
        output = subprocess.run(f'adb -s {d.serial} shell "dumpsys window windows | grep mCurrentFocus;dumpsys activity activities | grep mResumedActivity;dumpsys activity top | grep "ACTIVITY"" ', shell=True, text=True, check=True, capture_output=True).stdout

        _focusedRE = re.compile(r'mCurrentFocus=Window{.*?\s+(?P<package>[^\s]+)/(?P<activity>[^\s]+)\}')
        m = _focusedRE.search(output)
        if m:
            return dict(package=m.group('package'), activity=m.group('activity'))

        _recordRE = re.compile(r'mResumedActivity: ActivityRecord\{.*?\s+(?P<package>[^\s]+)/(?P<activity>[^\s]+)\s.*?\}')
        m = _recordRE.search(output)
        if m:
            package = m.group("package")

        _activityRE = re.compile(r'ACTIVITY (?P<package>[^\s]+)/(?P<activity>[^/\s]+) \w+ pid=(?P<pid>\d+)')
        ms = _activityRE.finditer(output)

        for m in ms:
            ret = dict(package=m.group('package'), activity=m.group('activity'), pid=int(m.group('pid')))
            if ret['package'] == package:
                return ret

        if ret:
            return ret

    raise OSError("Couldn't get focused app")


def try_times(
        attempt_amount: int | float,
        attempt_timeout: int | float = 0, # между попытками
        catch_exceptions: Iterable[Exception | Exception.__class__] = (Exception,),
        rais_exception: Exception | Exception.__class__ = None,
        default_result=None
):
    def wrapper(func):
        class NoResult:
            ...

        def inner_wrapper(*args, **kwargs):

            res = NoResult
            attempt_counter = 0

            while res == NoResult and attempt_counter < attempt_amount:
                try:
                    res = func(*args, **kwargs)
                except catch_exceptions as e:
                    time.sleep(attempt_timeout)
                    attempt_counter += 1

            if res != NoResult: return res
            if rais_exception is not None: raise rais_exception
            return default_result

        return inner_wrapper

    return wrapper


def log_activity(device: u2.Device, activity):
    try:
        if activity.uniq_code in os.listdir('activities'): return

        dir = f'activities/{activity.uniq_code}'
        os.mkdir(dir)
        with open(f'{dir}/display.xml', 'w+') as f:
            f.write(device.dump_hierarchy())
        with open(f'{dir}/activity.py', 'w+') as f:
            f.write(str(activity))
        device.screenshot(f'{dir}/screen.png')
    except Exception as e:
        print(str(e))
        print('CANT LOG')


def gen_name(gender=enums.Gender.FEMALE, region='ru'):
    if region == 'ru':
        person = Person(locale=locales.Locale.RU)
    else:
        person = Person(locale=locales.Locale.EN)

    return person.full_name(gender=gender)


def get_list_adb(bad_devices_125, all=False):
    while True:
        try:
            devices = []
            bad_devices = []
            out = subprocess.run(['adb', 'devices'], check=True, capture_output=True, text=True).stdout.split('\n')
            for line in out:
                regex = re.split(r'\t', line)
                if len(regex) == 2:
                    if regex[1] == 'device' and (all or (len(regex[0]) == 11 and regex[0] not in config.DEVICE_PAIRS.values() and regex[0] not in bad_devices_125)):
                        devices.append(regex[0])
                    else:
                        bad_devices.append(regex[0])
            break
        except Exception as e:
            print('EXCEPTION IN GET_LIST_ABD')
            print(e)
            print('_________________________')
            if isinstance(e, subprocess.SubprocessError):
                pass
    return devices, bad_devices


def replace_phone(text, use_normalize=False):
    if text:
        if use_normalize:
            text = normalize_wa_text(text)
        return re.sub(r'\+[\s\d()-]+\d', '{phone_replaced}', text)


# TODO find difference and remove one

def clen_numbers(numbers: list[str]):
    clear_number = lambda number: ''.join(x for x in number if x.isdigit())
    return [clear_number(number) for number in numbers]


def find_phone(text, use_normalize=False):
    if text:
        if use_normalize:
            text = normalize_wa_text(text)
        return normalize_phone(re.search(r'\+7\s\d{3}\s\d{3}-\d{2}-\d{2}', text).group(0))


def normalize_phone(text):
    if text:
        return re.sub(r'[\+\s-]', '', text)


def normalize_wa_text(text):
    if text:
        return normalize('NFKD', text)


def separate_limit(lim: int, max_lim: int):
    if lim > max_lim:
        return (max_lim,) * (lim // max_lim) + (lim % max_lim,)
    return (lim,)


def separate_sequence(seq: Sequence, lim: int):
    return tuple(seq[i: i + lim] for i in range(0, len(seq) - 1, lim))


def get_mac():
    if config.ENABLE_WEB_BACKUP:
        return 'WEB'
    else:
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))


def generator_yandex_eda():
    myset = []
    for e1 in ("e", "е"):
        for c1 in ("c", "с"):
            for E1 in ("E", "Е"):
                for a1 in ("a", "а"):
                    myset.append(f"Янд{e1}к{c1}.{E1}д{a1}")
    for a1 in ("a", "а"):
        for e1 in ("e", "е"):
            for E1 in ("E", "Е"):
                for a2 in ("a", "а"):
                    myset.append(f"Y{a1}nd{e1}x.{E1}d{a2}")
    return myset


def get_wa_contacts(d):
    wa_contacts = dict()
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/com.whatsapp/databases/wa.db \"\\\"select replace(jid, \'@s.whatsapp.net\', '') as phone, is_whatsapp_user as status from wa_contacts where phone != \'status@broadcast\';\\\"\"").output
    for row in out.split('\n')[:-1]:
        if '|' not in row:
            continue
        phone, status = row.split('|')
        wa_contacts[phone] = status
    return wa_contacts


def get_wa_messages(d, banned: False) -> dict:
    # хардкод чтобы не откатывать сообщения со статусом sent
    banned = False
    wa_messages = dict()
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"\\\"select replace(raw_string_jid, \'@s.whatsapp.net\', '') as phonee, case when status = 4 then 'sent' when status = 5 then 'delivered' when status = 13 then 'read' when status = 0 then 'not sent' else status end as st from chat_view as t1 inner join message as t2 on t1._id = t2.chat_row_id where from_me = 1 and message_type in (0, 1)\\\"\"").output
    for row in out.split('\n')[:-1]:
        if '|' not in row:
            continue
        phone, status = row.split('|')
        if wa_messages.get(phone) == 'not sent':
            continue
        wa_messages[phone] = status

    if banned:
        for phone in list(wa_messages.keys())[::-1]:
            status = wa_messages[phone]
            if status == 'not sent':
                continue
            elif status not in ('read', 'delivered'):
                wa_messages[phone] = 'not sent'
            else:
                break
    return wa_messages


def get_wa_group_messages(d) -> str:
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"\\\"select text_data from message where recipient_count > 1 and status in (4, 5, 13)\\\"\"").output
    return out

def get_wa_phone_status(d) -> dict:
    """Для получения статуса разосланных сообщений"""
    wa_messages = dict()
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"\\\"select replace(raw_string_jid, \'@s.whatsapp.net\', '') as phonee, case when status = 4 then 'sent' when status = 5 then 'delivered' when status = 13 then 'read' when status = 0 then 'not sent' else status end as st from chat_view as t1 inner join message as t2 on t1._id = t2.chat_row_id where from_me = 1 and message_type in (0, 1)\\\"\"").output
    for row in out.split('\n')[:-1]:
        if '|' not in row:
            continue
        phone, status = row.split('|')
        if wa_messages.get(phone) == 'not sent':
            continue
        wa_messages[phone] = status
    return wa_messages

def get_wa_answers(d) -> list[dict]:
    wa_answers = dict()
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"\\\"select replace(raw_string_jid, \'@s.whatsapp.net\', '') as phonee, text_data from chat_view as t1 inner join message as t2 on t1._id = t2.chat_row_id where from_me = 0 and message_type in (0, 1) order by t2._id desc\\\"\"").output
    for row in out.split('\n')[:-1]:
        if '|' not in row:
            continue
        phone, answer = row.split('|', maxsplit=1)
        if wa_answers.get(phone):
            if wa_answers[phone][0] < 5:
                wa_answers[phone][1].append(answer)
                wa_answers[phone][0] += 1
        else:
            # wa_answers[phone][0] - кол-во сообщений, список будет быстрее чем словарь
            wa_answers[phone] = [1, [answer]]
    wa_answers_income = []
    for phone, answer in wa_answers.items():
        wa_answers_income.append({'phone': phone, 'message': '\n'.join(answer[1][::-1])})
    return wa_answers_income


def delete_wa_answers(d):
    d.shell(f"su -c /data/local/sqlite3 /data/data/com.whatsapp/databases/msgstore.db \"\\\"update message set message_type = -1 where from_me = 0 and message_type in (0, 1)\\\"\"")


def set_proxy(d, host: str, port: int, username: str, password: str, type: int) -> str:
    port = str(port)
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/org.sandroproxy.drony/databases/drony.db \"\\\"select count(*) from proxy;\\\"\"").output
    # если в базе ничего нет, значит приложение только установили -> добавляем/обновляем прокси
    if out[0] == "0":
        insert = f"""insert into proxy (_id, proxy_id, network_id, type, host, port, domain_realm, username, password, active, auth_type, workstation, handshake_type, hand_type_https_trust_all) select 1,'{host + ':' + port}','NOT LISTED NETWORKS','manual','{host}',{port},null,'{username}','{password}',0,0,null,{type},0;"""
        d.shell(f"su -c /data/local/sqlite3 /data/data/org.sandroproxy.drony/databases/drony.db \"\\\"{insert}\\\"\"")
    else:
        d.shell(f"su -c /data/local/sqlite3 /data/data/org.sandroproxy.drony/databases/drony.db \"\\\"update proxy set proxy_id = '{host + ':' + port}',host = '{host}', port  = {port}, username = '{username}', password = '{password}', handshake_type = {type}, _id = 1, network_id = 'NOT LISTED NETWORKS', type = 'manual', domain_realm = null, active = 0, auth_type = 0, workstation = null, hand_type_https_trust_all = 0;\\\"\"")
    d.shell(f"su -c /data/local/sqlite3 /data/data/org.sandroproxy.drony/databases/drony.db \"\\\" update network set proxy_type = 'manual' where _id = 1;\\\"\"")
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/org.sandroproxy.drony/databases/drony.db \"\\\"select * from proxy;\\\"\"").output
    return out


def change_proxy_ip(url) -> bool:
    response = requests.get(
        url=url
    )
    return response.status_code == 200


def check_proxy(d, host: str, port: int, username: str, password: str, type: int) -> bool:
    port, type = str(port), str(type)
    out = d.shell(f"su -c /data/local/sqlite3 /data/data/org.sandroproxy.drony/databases/drony.db \"\\\"select host, port, username, password, handshake_type from proxy;\\\"\"").output
    return out[:-1].split('|') == [host, port, username, password, type]


def set_default_params(parent, child) -> None:
    """Для наследования настроек"""
    parent_attributes = parent.__dict__
    child_attributes = child.__dict__

    parent_keys = set(parent_attributes.keys())
    child_keys = set(child_attributes.keys())

    common_keys = parent_keys.intersection(child_keys)

    for key in common_keys:
        if child_attributes[key] is None:
            child.__setattr__(name=key, value=parent_attributes[key])


def randomize_samsung_contacts(d):
    amount_contacts = None
    for x in range(5):
        try:
            out = d.shell(f"su -c /data/local/sqlite3 /data/data/com.samsung.android.providers.contacts/databases/contacts2.db \"\\\"select _id, max(contact_last_updated_timestamp) from contacts\\\"\"").output
            if '|' not in out:
                print('NO SAMSUNG CONTACTS')
                return None
            amount_contacts, last_updated_contact_timestamp = [int(i) for i in out.strip('\n').split('|')]

            for y in range(1, amount_contacts + 1):
                # Новое время будет равно "последняя дата обновления" - 90 дней - "случайное кол-во дней от 1 до 90" - случайное кол-во микросекунд от 1 до 10. В базе контактов время хранится в микросекундах
                new_time = last_updated_contact_timestamp - 7776000000 - random.randint(1, 90) * 86400000 + random.randint(1, 10)
                d.shell(f"su -c /data/local/sqlite3 /data/data/com.samsung.android.providers.contacts/databases/contacts2.db \"\\\"update contacts set contact_last_updated_timestamp = {new_time} where _id = {x}\\\"\"")
        except ValueError:
            continue
    return amount_contacts


def is_now_in_interval(min_hour: int, max_hour: int) -> bool:
    now = datetime.now()
    return min_hour <= now.hour < max_hour


def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            future = None
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    if future and not future.done():
                        future.cancel()  # Отмена выполнения функции
                    raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
                return result
        return wrapper
    return decorator


def divide_chunks(obj, number):
    """ Делит список на списки, состоящие из number записей """
    for i in range(0, len(obj), number):
        yield obj[i:i + number]


def generate_name_by_pattern(obj, to_group: bool = True, to_community: bool = True):
    """ Генерирует названия групп и коммьюнити по шаблону """

    rus_chars = '1234567890йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ'
    word_length = 16

    community_pattern = obj.community_pattern
    group_pattern = obj.group_pattern
    group_left = ''
    group_right = ''
    community_left = ''
    community_right = ''
    for _ in range(word_length // 2):
        group_left += random.choice(rus_chars)
        group_right += random.choice(rus_chars)
        community_left += random.choice(rus_chars)
        community_right += random.choice(rus_chars)

    if to_group:
        obj.group_name = group_pattern.format(left=group_left, name=obj.group_name_original, right=group_right)
    if to_community:
        obj.community_name = community_pattern.format(left=community_left, name=obj.community_name, right=community_right)


class GroupImage:
    _FOLDER = f'{os.getcwd()}/services/photos/group'

    @classmethod
    def download(cls, image: str, serial: str) -> str:
        """ Скачивание картинки с CDN для рассылки по группам """
        SelectelCDN().download_file(image,
                                    f'{cls._FOLDER}/{serial}-{image}',
                                    'skillbox_womans/group', custom_filename=True)
        return f'{serial}-{image}'

    @classmethod
    def delete(cls, serial: str) -> None:
        """ Удаление картинки после итерации в main для рассылки по группам """
        try:
            for filename in os.listdir(cls._FOLDER):
                if serial in filename:
                    os.remove(f'{cls._FOLDER}/{filename}')
        except: ...

    @classmethod
    def upload(cls, device: u2.Device, image: str) -> None:
        """ Загрузка картинки на телефон """
        device.push(f'{cls._FOLDER}/{image}', '/storage/emulated/0/DCIM/Camera/')
        device.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM/Camera/{image}')

