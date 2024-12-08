import datetime
import time

import requests

from . import activate_exceptions
from .base_activator import BaseActivator
from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS


class DropSms(BaseActivator):
    NAME = ActivatorName.DROP_SMS

    def get_phone(self, service='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)

        while True:
            try:
                response = requests.get(
                    url="https://api.dropsms.cc/stubs/handler_api.php",
                    params=(
                        ("action", "getNumber"),
                        ("api_key", KeyActivator.DROP_SMS),
                        ("service", service),
                        ("country", REGIONS.get_code(country_name=self.region, activator_name='sms_activate'))
                    )
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if response.status_code == 200 and (response.text == "NO_NUMBERS" or response.text == 'NO_BALANCE'):
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
