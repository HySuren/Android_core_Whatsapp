import time
import datetime
import requests

from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from .base_activator import BaseActivator
from . import activate_exceptions


class SmsHub(BaseActivator):

    NAME = ActivatorName.SMS_HUB

    def get_phone(self, srvice='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)
        if REGIONS.get_code(self.region, self.NAME) != '0':
            self.operator = 'any'

        while True:
            try:
                response = requests.post(
                    url="https://smshub.org/stubs/handler_api.php?",
                    params={
                        "api_key": KeyActivator.SMS_HUB,
                        "action": "getNumber",
                        "service": srvice,
                        "country": REGIONS.get_code(self.region, ActivatorName.SMS_ACTIVATE),
                        "operator": self.operator
                    },
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if "access_number" in response.text.lower():
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.GetNumberTimeoutException(Exception)

            time.sleep(3)

            if "no_balance" in response.text.lower() or "whatsapp_not_available" in response.text.lower():
                raise activate_exceptions.BuyNumberException(Exception)

        id, phone = [item.replace("$", "") for item in response.text.split(":")[1:]]

        len_code = len(str(REGIONS.get_country_code(self.region)))
        code = phone[:len_code]
        phone = phone[len_code:]
        return id, code, phone

    def get_code(self, id: int, timeout=60):
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            response = requests.post(
                "https://smshub.org/stubs/handler_api.php?",
                params={
                    "api_key": KeyActivator.SMS_HUB,
                    "action": "getStatus",
                    "id": id
                })

            if "status_cancel" in response.text.lower():
                raise activate_exceptions.CancelNumber(Exception)

            time.sleep(3)

            if "status_ok" in response.text.lower():
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.TimeOutExceptionWaitCode(Exception)

        code = response.text.split(':')[1].replace("'", "")
        return code

    def phone_confirm(self, id: int):
        self._update_number_status(id, status=6)
        return True

    def sms_confirm(self, id: int):
        self._update_number_status(id, status=1)
        return True

    def phone_cancel(self, id: int):
        self._update_number_status(id, status=8)
        return True

    def phone_ban(self, id: int):
        return self.phone_cancel(id)

    def _update_number_status(self, id: int, status: int):
        """
        1 сообщить о готовности номера (смс на номер отправлено)
        3 запросить еще один код (бесплатно)
        6 завершить активацию *
        8 сообщить о том, что номер использован и отменить активацию
        """
        response = requests.post(
            url="https://smshub.org/stubs/handler_api.php?",
            params={
                "api_key": KeyActivator.SMS_HUB,
                "action": "setStatus",
                "id": id,
                "status": status
            },
        )
        return response.text

    @classmethod
    def check_balance(self):
        response = requests.get(
            'https://api.smshub.org/stubs/handler_api.php',
            {
                "api_key": KeyActivator.SMS_HUB,
                "action": "getBalance"
            }
        )
        balance = response.text.split(':')[1].replace("'", "")
        if float(balance) > 5000:
            return True
        else:
            return False

