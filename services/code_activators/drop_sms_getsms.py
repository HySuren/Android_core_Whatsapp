import datetime
import time

import requests
import httpx

# import core.script_iterator
from . import activate_exceptions
from .base_activator import BaseActivator
from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from services.utils import timeout

class DropSmsGetsms(BaseActivator):
    NAME = ActivatorName.DROP_SMS_GETSMS

    def get_phone(self,  obj, service='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)
        obj.logger.info(f'starting get_phone')
        while True:
            try:
                reg_code = REGIONS.get_code(country_name=self.region, activator_name='sms_activate')
                obj.logger.info(f'got region code for country')
                url = "https://api.dropsms.cc/stubs/handler_api.php"
                params = {
                    "action": "getNumber",
                    "api_key": KeyActivator.DROP_SMS,
                    "service": service,
                    "country": reg_code,
                    "proxy_geo": "eng"
                }
                with httpx.Client() as client:
                    response = client.get(url, params=params, timeout=2.0)

                obj.logger.info(f'request end with {response.status_code} status_code')
                if obj.drop_sms_response_enable:
                    obj.logger.info(f'logging drop answer')
                    if response.status_code >= 500:
                        obj.device_info.params['drop_sms_response'].append({"status_code": response.status_code, "response_text": "HTML_ERROR"})
                    else:
                        obj.device_info.params['drop_sms_response'].append({"status_code": response.status_code, "response_text": response.text})
            except Exception as e:
                obj.logger.info(f'exception occured')
                if isinstance(e, httpx.TimeoutException) or isinstance(e, httpx.RequestError):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if response.status_code == 200 and (response.text == "NO_NUMBERS" or response.text == 'NO_BALANCE'):
                obj.logger.info(f'checking timeout for drop')
                if datetime.datetime.now() >= future:
                    raise activate_exceptions.GetNumberTimeoutException(Exception)

                time.sleep(1)

                continue

            if response.status_code in (400, 500, 522) or '<!DOCTYPE html>' in response.text:
                raise activate_exceptions.BuyNumberException(response.text)

            break
        res = response.text.split(':')
        id = res[1]
        phone = str(res[2]).replace("+", "")
        len_code = len(str(REGIONS.get_country_code(self.region)))
        code = phone[:len_code]
        phone = phone[len_code:]
        return id, code, phone

    def get_code(self, id: str, timeout=60):
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            try:
                response = requests.get(url="https://api.dropsms.cc/stubs/handler_api.php", params=(("action", "getStatus"), ("api_key", KeyActivator.DROP_SMS), ("id", id)))
                try:
                    answer = response.text
                    if 'error' in answer or 'timed out' in answer:
                        code = None
                    else:
                        code = answer.split(':')[1]
                        if len(code) != 6:
                            code = None

                except IndexError:
                    code = None

                if code is None:

                    if datetime.datetime.now() >= future:
                        raise activate_exceptions.TimeOutExceptionWaitCode(Exception)

                    time.sleep(1)

                    continue
                break
            except requests.exceptions.ConnectionError:
                raise activate_exceptions.GetActivationCodeException()

        return code

    def phone_confirm(self, id: int):
        ...

    def sms_confirm(self, id: int):
        ...

    def phone_cancel(self, id: int):
        ...

    def phone_ban(self, id: int):
        ...

    def _update_number_status(self, id: int, status):
        ...

    @classmethod
    def check_balance(self):
        ...
