import time
import datetime
import requests

from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from .base_activator import BaseActivator
from . import activate_exceptions


class SmsActivateRent(BaseActivator):

    NAME = ActivatorName.SMS_ACTIVATE_RENT

    def get_phone(self, srvice='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)
        if REGIONS.get_code(self.region, ActivatorName.SMS_ACTIVATE) != '0':
            self.operator = 'any'

        while True:
            try:
                response = requests.post(
                    url="https://sms-activate.org/stubs/handler_api.php?",
                    params={
                        "api_key": KeyActivator.SMS_ACTIVATE,
                        "action": "getRentNumber",
                        "service": srvice,
                        "rent_time": 4,
                        "country": REGIONS.get_code(self.region, ActivatorName.SMS_ACTIVATE),
                        "operator": self.operator
                    },
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if response.json()['status'] == 'success':
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.GetNumberTimeoutException(Exception)

            time.sleep(3)

            if "no_balance" in response.text.lower() or "whatsapp_not_available" in response.text.lower():
                raise activate_exceptions.BuyNumberException(Exception)

        id = response.json()['phone']['id']
        phone = response.json()['phone']['number']

        len_code = len(str(REGIONS.get_country_code(self.region)))
        code = phone[:len_code]
        phone = phone[len_code:]
        return id, code, phone

    def get_code(self, id: int, timeout=60):
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            response = requests.post(
                "https://sms-activate.ru/stubs/handler_api.php?",
                params={
                    "api_key": KeyActivator.SMS_ACTIVATE,
                    "action": "getRentStatus",
                    "id": id
                })

            if "status_cancel" in response.text.lower():
                raise activate_exceptions.CancelNumber(Exception)

            time.sleep(3)

            if response.json()['status'] == 'success':
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.TimeOutExceptionWaitCode(Exception)

        text = list(response.json()['values'].values())[-1]['text']
        code = int(text.replace('Your WhatsApp code: ', '').strip()[:7].replace('-', ''))
        return code

    def phone_cancel(self, id: int):
        self._update_number_status(id, status=2)
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
            url="https://sms-activate.org/stubs/handler_api.php?",
            params={
                "api_key": KeyActivator.SMS_ACTIVATE,
                "action": "setRentStatus",
                "id": id,
                "status": status
            },
        )
        return response.text

    @classmethod
    def check_balance(self):
        response = requests.get(
            'https://api.sms-activate.org/stubs/handler_api.php',
            {
                "api_key": KeyActivator.SMS_ACTIVATE,
                "action": "getBalance"
            }
        )
        balance = response.text.split(':')[1].replace("'", "")
        if float(balance) > 5000:
            return True
        else:
            return False

