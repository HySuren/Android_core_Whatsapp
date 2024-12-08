import time
import datetime
import requests
from services import utils

from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from .base_activator import BaseActivator
from . import activate_exceptions


class VakSms(BaseActivator):

    NAME = ActivatorName.VAK_SMS

    def get_phone(self, service='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)
        params = (
            ("apiKey", KeyActivator.VAK_SMS),
            ("service", service),
            ("country", REGIONS.get_code(self.region, self.NAME)),
        )
        if self.operator != 'any' and self.operator is not None:
            params += (("operator", self.operator),)

        while True:
            try:
                response = requests.get(
                    url=f"https://vak-sms.com/api/getNumber",
                    params=params
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e
            error = response.json().get("error")

            if error:
                if error == "noNumber":

                    if datetime.datetime.now() >= future:
                        raise activate_exceptions.GetNumberTimeoutException

                    time.sleep(3)
                    continue

                raise activate_exceptions.BuyNumberException(response.text)

            break
        phone = str(response.json().get("tel")).replace("+", "")

        len_code = len(str(REGIONS.get_country_code(self.region)))
        code = phone[:len_code]
        phone = phone[len_code:]
        return response.json()["idNum"], code, phone

    def get_code(self, id: int, timeout=60):
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            response = requests.get(
                url=f"https://vak-sms.com/api/getSmsCode",
                params=(
                    ("apiKey", KeyActivator.VAK_SMS),
                    ("idNum", id)
                )
            )
            error = response.json().get("error")

            if error:
                raise activate_exceptions.GetActivationCodeException
            code = response.json().get("smsCode")

            if code is None:

                if datetime.datetime.now() >= future:
                    raise activate_exceptions.GetActivationCodeException
                time.sleep(5)

                continue

            break

        return code

    def phone_confirm(self, id: int): ...

    def sms_confirm(self, id: int): ...

    def phone_cancel(self, id: int):
        self._update_number_status(id, status='end')
        return True

    def phone_ban(self, id: int):
        self._update_number_status(id, status='bad')
        return True

    @utils.try_times(attempt_amount=5, attempt_timeout=5, catch_exceptions=requests.exceptions.ConnectionError)
    def _update_number_status(self, id: int, status):
        response = requests.get(
            url="https://vak-sms.com/api/setStatus",
            params=(
                ("apiKey", KeyActivator.VAK_SMS),
                ("idNum", id),
                ("status", status)
            )
        )

        if response.status_code == 400:
            raise activate_exceptions.UpdateNumberStatusException(response.text)

        return response.text

    @classmethod
    def check_balance(self):
        response = requests.get('https://vak-sms.com/api/getBalance', {"api_key": KeyActivator.VAK_SMS})
        balance = response.json()["balance"]
        if float(balance) > 6:
            return True
        else:
            return False
