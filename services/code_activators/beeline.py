import time
import datetime
import requests

from .config import ActivatorTimeout, ActivatorName
from .base_activator import BaseActivator
from . import activate_exceptions


class SMS_Beeline(BaseActivator):
    NAME = ActivatorName.SMS_BEELINE
    
    def get_phone(self, srvice='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)

        while True:
            try:
                response = requests.get(
                    url="https://wa2.qeepmail.ru/api/v2/beeline/get-phone",
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if response.status_code == 200:
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.GetNumberTimeoutException(Exception)

            time.sleep(1)

        response = response.json()
        id = response.get('id')
        code = response.get('phone')[:1]
        num = response.get('phone')[1:]
        return id, code, num

    def get_code(self, id: int, timeout=60):
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            response = requests.get(
                url="https://wa2.qeepmail.ru/api/v2/beeline/get-code",
                params={"id": id}
            )

            if response.status_code == 200:
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.TimeOutExceptionWaitCode(Exception)
            
            time.sleep(1)

        response_code = response.json()
        return response_code

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
        ...

