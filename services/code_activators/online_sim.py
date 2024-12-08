import time
import datetime
import requests

from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from .base_activator import BaseActivator
from . import activate_exceptions




class OnlineSim(BaseActivator):

    NAME = ActivatorName.ONLINE_SIM

    def get_number(self, service='wa'):
        response__exceptions = {
            "ERROR_WRONG_KEY": activate_exceptions.BuyNumberException,
            "EXCEEDED_CONCURRENT_OPERATIONS": activate_exceptions.BuyNumberException,
            "WARNING_NO_NUMS": activate_exceptions.BuyNumberException
        }
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)

        while True:
            try:
                response = requests.get(
                    url=f"https://onlinesim.ru/api/getNum.php?apikey={KeyActivator.ONLINE_SIM}&service=Whatsapp&country={REGIONS.get_code(self.region, self.NAME)}",
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if response.json()["response"] == "NO_NUMBER":
                if datetime.datetime.now() > future:
                    raise activate_exceptions.GetNumberTimeoutException(Exception)

                time.sleep(1)
                continue

            exception = response__exceptions.get(response.json()["response"])

            if exception:
                raise exception

            tzid = response.json().get("tzid")

            if tzid:
                break

            time.sleep(1)

            if datetime.datetime.now() >= future:
                raise activate_exceptions.TimeOutExceptionWaitCode

        while True:
            response = requests.get(
                url=f"https://onlinesim.ru/api/getState.php?apikey={KeyActivator.ONLINE_SIM}&tzid={tzid}"
            )

            if type(response.json()) != list and response.json().get("response"):
                exception = response__exceptions.get(response.json()["response"])

                if exception:
                    raise exception

                time.sleep(1)

            phone = response.json()[0]["number"]

            if phone:
                break

        phone = phone.replace("+", "")
        len_code = len(str(REGIONS.get_country_code(self.region)))
        code = phone[:len_code]
        phone = phone[len_code:]
        return tzid, code, phone

    def get_code(self, id: int, timeout=60):
        response__exceptions = {
            "ERROR_WRONG_KEY": activate_exceptions.GetActivationCodeException,
            "EXCEEDED_CONCURRENT_OPERATIONS": activate_exceptions.GetActivationCodeException,
            "NO_NUMBER": activate_exceptions.GetActivationCodeException,
            "WARNING_NO_NUMS": activate_exceptions.GetActivationCodeException
        }
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            response = requests.get(
                url=f"https://onlinesim.ru/api/getState.php?apikey={KeyActivator.ONLINE_SIM}&tzid={id}"
            )

            if type(response.json()) != list and response.json().get("response"):
                exception = response__exceptions.get(response.json()["response"])

                if exception:
                    raise exception

                time.sleep(1)

            code = response.json()[0].get("msg")
            if code:
                return code

            time.sleep(1)

            if datetime.datetime.now() >= future:
                raise activate_exceptions.TimeOutExceptionWaitCode(Exception)

    def phone_confirm(self, id: int):
        self._update_number_status(id, status='setOperationOk')
        return True

    def sms_confirm(self, id: int): ...

    def phone_cancel(self, id: int): ...

    def phone_ban(self, id: int): ...

    def _update_number_status(self,  id: int, status: str):
        response__exceptions = {
            "ERROR_WRONG_TZID": activate_exceptions.UpdateNumberStatusException,
            "NO_COMPLETE_TZID": activate_exceptions.UpdateNumberStatusException
        }
        response = requests.get(
            url=f"https://onlinesim.ru/api/{status}.php?apikey={KeyActivator.ONLINE_SIM}&tzid={id}"
        )

        exception = response__exceptions.get(response.json()["response"])

        if exception:
            raise exception

        return response.text

    @classmethod
    def check_balance(self): ...
