import enum
import math
from typing import NamedTuple, Any

import requests
from requests.exceptions import RequestException, ReadTimeout
from urllib3.exceptions import ProtocolError

from iterator_models import Config, Account, Campaign, Messages, Contact, GeneratedAccountInfo, Contacts, Proxy, WarmStatus
from services import utils
from config import DB_MODE
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='whatsapp.log')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)

logging.getLogger().addHandler(stdout_handler)

AUTH = 'ea92c1c9-86f0-4ecc-9e2a-115f1499290a'

if DB_MODE == 'prod':
    HOST = f'https://wa3.qeepmail.ru'
else:
    # порт запущенной API на локалке
    HOST = f'http://127.0.0.1:8008/dev'


class ManyTaskRetryException(Exception): ...


class NoResultException(Exception): ...


CATCH_EXCEPTIONS_FOR_TASK = (ConnectionError, ProtocolError, RequestException, NoResultException, ReadTimeout)
CATCH_EXCEPTIONS = (ConnectionError, ProtocolError, RequestException, ManyTaskRetryException, ReadTimeout)


class URL(NamedTuple):
    url: str
    method: Any                 # TODO
    timeout: float | None = 60  # Ограничение, чтобы не зависнуть на запросе


class ROUTES:
    GET_CONFIG                   = URL(HOST + '/config',                                          requests.get)
    GET_MESSAGE_ANSWER           = URL(HOST + '/find-answers',                                    requests.get)
    GET_ACCOUNT_WARM             = URL(HOST + '/get-account-warm?serial={}',                      requests.get)
    GET_MESSAGES_WARM            = URL(HOST + '/get-messages-warm',                               requests.get)
    GET_CONTACTS_WARM            = URL(HOST + '/get-contacts-warm?account_id={}',                 requests.get)
    GET_ACCOUNT                  = URL(HOST + '/get-account?farm={}&serial={}&serial_binding={}', requests.get)
    GET_ACCOUNT_W_PROXY          = URL(HOST + '/get-account?farm={}&serial={}&serial_binding={}&proxy_enable={}', requests.get)
    # GET_ACCOUNT                  = URL(HOST + '/get-account?farm={}&serial={}&serial_binding={}&iter_sleep=15', requests.get)
    GET_ACCOUNT_TO_SCAN_WEB      = URL(HOST + '/get-account-to-scan-web?serial={}',               requests.get)
    GET_CAMPAIGN                 = URL(HOST + '/get-campaign-by-account?account_id={}',           requests.get)
    GET_MESSAGES                 = URL(HOST + '/get-messages',                                    requests.get)
    GET_CAMPAIGN_TO_REG          = URL(HOST + '/get-campaign-to-reg?serial={}&farm={}&is_campaign_test={}',           requests.get)
    CREATE_ACCOUNT               = URL(HOST + '/insert-account',                                  requests.post)
    CREATE_ITERATION             = URL(HOST + '/insert-iteration',                                requests.post)
    CREATE_OUTCOME_MESSAGES      = URL(HOST + '/insert-outcome-messages',                         requests.post)
    CREATE_WARM_OUTCOME_MESSAGES      = URL(HOST + '/insert-warm-outcome-messages',               requests.post)
    CREATE_INCOME_MESSAGES       = URL(HOST + '/insert-income-messages',                          requests.post)
    SET_ACCOUNT_IN_WORK          = URL(HOST + '/set-account-in-work',                             requests.patch)
    SET_ACCOUNT_BANNED           = URL(HOST + '/set-account-banned',                              requests.patch)
    UPDATE_DEVICE                = URL(HOST + '/update-device',                                   requests.put)
    UPDATE_ACCOUNT               = URL(HOST + '/update-account',                                  requests.put)
    UPDATE_INVALID_MESSAGES      = URL(HOST + '/update-invalid-phones',                           requests.put)
    UPDATE_WARM_INVALID_MESSAGES      = URL(HOST + '/update-warm-invalid-phones',                 requests.put)
    UPDATE_NOT_SENT_MESSAGES     = URL(HOST + '/update-not-sent-phones',                          requests.put)
    UPDATE_WARM_NOT_SENT_MESSAGES     = URL(HOST + '/update-warm-not-sent-phones',                requests.put)
    GENERATE_RANDOM_ACCOUNT_INFO = URL(HOST + '/generate-random-account-info',                    requests.get)
    GET_GENERATED_ACCOUNT_INFO   = URL(HOST + '/get-generated-account-info?id={}',                requests.get)
    GET_CONTACTS                 = URL(HOST + '/get-contacts?account_id={}&campaign_id={}',       requests.get)
    GET_PROXY                    = URL(HOST + '/get-proxy?&serial={}',                            requests.get)
    GET_PROXY_WITH_COUNTRY       = URL(HOST + '/get-proxy?&serial={}&country={}',                 requests.get)
    GET_PROXY_WITH_COMPANY       = URL(HOST + '/get-proxy?&serial={}&campaign_id={}',             requests.get)
    GET_WARM_STATUS              = URL(HOST + '/get-warm-status?&campaign_id={}&account_id={}',   requests.get)
    GET_WARM_PHONES              = URL(HOST + '/warm-phones',   requests.get)
    GET_CAMPAIGN_BY_SERIAL       = URL(HOST + '/get-campaign-by-serial?serial={}',                requests.get)


class RequestMethods(enum.Enum):
    GET = requests.get
    SET = requests.patch
    UPDATE = requests.put
    CREATE = requests.post
    DELETE = requests.delete


@utils.try_times(attempt_amount=600, attempt_timeout=1, catch_exceptions=CATCH_EXCEPTIONS_FOR_TASK, rais_exception=ManyTaskRetryException)
def wait_for_task(uuid):
    response = requests.get(f'{HOST}/task?uuid={uuid}', headers={'Authorization': AUTH})
    if response.status_code == 200:
        return response.json()
    if response.status_code == 201:
        return
    if response.status_code == 502:
        ...
    if response.status_code == 500:
        raise Exception(response.json()['error'])
    raise NoResultException


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_config() -> Config | None:
    route = ROUTES.GET_CONFIG
    response = route.method(route.url, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_config.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return Config(**item)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def update_device(serial: str, farm: str | None) -> None:
    json = {
        'serial': serial,
        'farm': farm
    }
    route = ROUTES.UPDATE_DEVICE
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{update_device.__name__}:\nrequests: {route}\nresponse: {uuid}")
    wait_for_task(uuid)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_account_warm(serial) -> Account | None:
    route = ROUTES.GET_ACCOUNT_WARM
    response = route.method(route.url.format(serial), headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_account_warm.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if account := wait_for_task(uuid):
        return Account(**account)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_messages_warm() -> Messages | None:
    route = ROUTES.GET_MESSAGES_WARM
    response = route.method(route.url, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_messages_warm.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if items := wait_for_task(uuid):
        return Messages(messages_to_send=items['messages'])


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_phones_warm(campaign_id) -> list[str] | None:
    route = ROUTES.GET_WARM_PHONES
    response = route.method(route.url, headers={'Authorization': AUTH}, params={'campaign_id': campaign_id},
                            timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_phones_warm.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if items := wait_for_task(uuid):
        return items


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_contacts_warm(account_id) -> list[Contact] | None:
    route = ROUTES.GET_CONTACTS_WARM
    response = route.method(route.url.format(account_id), headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_contacts_warm.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if items := wait_for_task(uuid):
        contacts = []
        for item in items:
            contacts.append(Contact(**item))
        return contacts


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_account(farm, serial, serial_binding=True, proxy_enable=False) -> Account | None:
    if proxy_enable:
        route = ROUTES.GET_ACCOUNT_W_PROXY
        formatted = route.url.format(farm, serial, serial_binding, proxy_enable)
    else:
        route = ROUTES.GET_ACCOUNT
        formatted = route.url.format(farm, serial, serial_binding)
    response = route.method(formatted, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_account.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if account := wait_for_task(uuid):
        return Account(**account)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_account_to_scan_web(serial) -> Account | None:
    route = ROUTES.GET_ACCOUNT_TO_SCAN_WEB
    response = route.method(route.url.format(serial), headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_account_to_scan_web.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if account := wait_for_task(uuid):
        return Account(**account)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_campaign_by_account(account) -> Campaign | None:
    route = ROUTES.GET_CAMPAIGN
    response = route.method(route.url.format(account.id), headers={'Authorization': AUTH}, timeout=route.timeout)
    print('[NO AUTOTESTS] RESPONSE FROM GET_CAMPAIGN', response.status_code, response.text)
    uuid = response.json()['uuid']
    logging.info(f"{get_campaign_by_account.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return Campaign(**item)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_messages(campaign, limit, domain, account) -> Messages | None:

    json = {
        'campaign': dict(campaign),
        'account': dict(account),
        'limit': limit,
        'domain': domain,
    }
    route = ROUTES.GET_MESSAGES
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_messages.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if items := wait_for_task(uuid):
        return Messages(messages_to_send=items['messages'], images=items['images'])


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def set_account_in_work(account, in_work) -> None:
    json = {
        'account_id': account.id,
        'in_work': in_work,
    }
    route = ROUTES.SET_ACCOUNT_IN_WORK
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{set_account_in_work.__name__}:\nrequests: {route}\nresponse: {uuid}")
    wait_for_task(uuid)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_campaign_to_reg(serial, farm, is_campaign_test) -> Campaign | None:
    route = ROUTES.GET_CAMPAIGN_TO_REG
    response = route.method(route.url.format(serial, farm, is_campaign_test), headers={'Authorization': AUTH},
                            timeout=route.timeout)
    print('RESPONSE FROM GET_CAMPAIGN_TO_REG', response.status_code, response.text)
    uuid = response.json()['uuid']
    logging.info(f"{get_campaign_to_reg.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return Campaign(**item)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def insert_account(account, campaign) -> int:
    json = {
        'account': dict(account),
        'campaign': dict(campaign),
    }
    route = ROUTES.CREATE_ACCOUNT
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{insert_account.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return item.get('account_id')


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def update_account(account) -> None:
    route = ROUTES.UPDATE_ACCOUNT
    response = route.method(route.url, json=dict(account), headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{update_account.__name__}:\nrequests: {route}\nresponse: {uuid}")
    wait_for_task(uuid)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def insert_iteration(type, serial, campaign_id, account_id, ip, reinstall_wa,
                     reg_aggregator=None, reg_country=None, reg_operator=None, reg_phones_used=None, device_info=None) -> int:
    if device_info is None:
        device_info = {}
    json = {
        'type': type,
        'serial': serial,
        'campaign_id': campaign_id,
        'account_id': account_id,
        'ip': ip,
        'reinstall_wa': reinstall_wa,
        'reg_aggregator': reg_aggregator,
        'reg_country': reg_country,
        'reg_operator': reg_operator,
        'reg_phones_used': reg_phones_used,
        'device_info': device_info
    }
    route = ROUTES.CREATE_ITERATION
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{insert_iteration.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return item.get('iteration_id')


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def set_account_banned(account) -> None:
    route = ROUTES.SET_ACCOUNT_BANNED
    response = route.method(route.url, json={'account_id': account.id}, headers={'Authorization': AUTH},
                            timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{set_account_banned.__name__}:\nrequests: {route}\nresponse: {uuid}")
    wait_for_task(uuid)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def __insert_messages(route, messages, iteration_id):
    messages_dicts = [dict(msg) for msg in messages]
    json = {
        'messages': messages_dicts,
        'iteration_id': iteration_id,
    }
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{__insert_messages.__name__}:\nrequests: {route}\nresponse: {uuid}")
    wait_for_task(uuid)


def insert_outcome_messages(messages, iteration_id, is_warm=False) -> None:
    if is_warm:
        __insert_messages(ROUTES.CREATE_WARM_OUTCOME_MESSAGES, messages, iteration_id)
    else:
        __insert_messages(ROUTES.CREATE_OUTCOME_MESSAGES, messages, iteration_id)


def insert_income_messages(messages, iteration_id) -> None:
    __insert_messages(ROUTES.CREATE_INCOME_MESSAGES, messages, iteration_id)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def __update_messages(route, messages) -> None:
    messages_dicts = [dict(msg) for msg in messages]
    response = route.method(route.url, json={'messages': messages_dicts}, headers={'Authorization': AUTH},
                            timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{__update_messages.__name__}:\nrequests: {route}\nresponse: {uuid}")
    wait_for_task(uuid)


def update_not_valid_phones(messages) -> None:
    __update_messages(ROUTES.UPDATE_INVALID_MESSAGES, messages)


def update_not_sent_messages(messages) -> None:
    __update_messages(ROUTES.UPDATE_NOT_SENT_MESSAGES, messages)


def update_warm_not_valid_phones(messages) -> None:
    __update_messages(ROUTES.UPDATE_WARM_INVALID_MESSAGES, messages)


def update_warm_not_sent_messages(messages) -> None:
    __update_messages(ROUTES.UPDATE_WARM_NOT_SENT_MESSAGES, messages)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def find_answers(messages, campaign_id, domain, account_name) -> Messages | None:
    json = {
        'messages': [dict(msg) for msg in messages],
        'campaign_id': campaign_id,
        'domain': domain,
        'account_name': account_name
    }
    route = ROUTES.GET_MESSAGE_ANSWER
    response = route.method(route.url, json=json, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{find_answers.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if items := wait_for_task(uuid):
        return Messages(messages_to_send=items['messages'])


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def generate_random_account_info() -> GeneratedAccountInfo:
    route = ROUTES.GENERATE_RANDOM_ACCOUNT_INFO
    response = route.method(route.url, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{generate_random_account_info.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return GeneratedAccountInfo(**item)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_generated_account_info(id) -> GeneratedAccountInfo:
    route = ROUTES.GET_GENERATED_ACCOUNT_INFO
    response = route.method(route.url.format(id), headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_generated_account_info.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return GeneratedAccountInfo(**item)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_contacts(account_id, campaign_id) -> Contacts:
    route = ROUTES.GET_CONTACTS
    response = route.method(route.url.format(account_id, campaign_id), headers={'Authorization': AUTH},
                            timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_contacts.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return Contacts(**item)


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_proxy(serial, country=None, campaign_id=None) -> Proxy | None:
    if country:
        route = ROUTES.GET_PROXY_WITH_COUNTRY
        formatted = route.url.format(serial, country)
    elif campaign_id:
        route = ROUTES.GET_PROXY_WITH_COMPANY
        formatted = route.url.format(serial, campaign_id)
    else:
        route = ROUTES.GET_PROXY
        formatted = route.url.format(serial)
    response = route.method(formatted, headers={'Authorization': AUTH}, timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_proxy.__name__}:\nrequests: {route}\nresponse: {uuid}")
    proxy = wait_for_task(uuid)
    if proxy and proxy['host']:
        return Proxy(**proxy)
    return None


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_warm_status(campaign_id: int, account_id:int) -> WarmStatus:
    route = ROUTES.GET_WARM_STATUS
    response = route.method(route.url.format(campaign_id, account_id), headers={'Authorization': AUTH},
                            timeout=route.timeout)
    uuid = response.json()['uuid']
    logging.info(f"{get_warm_status.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return WarmStatus(**item).warm_enabled


@utils.try_times(attempt_amount=3, attempt_timeout=10, catch_exceptions=CATCH_EXCEPTIONS)
def get_campaign_by_serial(serial: str) -> Campaign | None:
    route = ROUTES.GET_CAMPAIGN_BY_SERIAL
    response = route.method(route.url.format(serial), headers={'Authorization': AUTH}, timeout=route.timeout)
    print('[AUTOTESTS] RESPONSE FROM GET_CAMPAIGN_BY_SERIAL', response.status_code, response.text)
    uuid = response.json()['uuid']
    logging.info(f"{get_campaign_by_serial.__name__}:\nrequests: {route}\nresponse: {uuid}")
    if item := wait_for_task(uuid):
        return Campaign(**item)
