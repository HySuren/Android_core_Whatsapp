
import time
import datetime
import requests

from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from .base_activator import BaseActivator
from . import activate_exceptions

"""
'any (any operator)'
'019'
'activ (virt10)'
'altel (virt11)'
'beeline (virt1)'
'claro'
'ee'
'globe'
'kcell (virt12)'
'lycamobile (virt14)'
'matrix'
'megafon (virt3)'
'mts (virt2)'
'orange'
'pildyk'
'play'
'redbullmobile'
'rostelecom (virt5)'
'smart'
'sun (virt8)'
'tele2 (virt4)'
'three'
'tigo'
'tmobile'
'tnt (virt9)'
'virginmobile'
'vodafone (virt15)'
'yota (virt16)'
'zz'
"""


class FiveSim(BaseActivator):
    NAME = ActivatorName.FIVE_SIM

    def get_phone(self, service='wa'):
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)

        while True:
            try:
                response = requests.get(
                    url=f"https://5sim.net/v1/user/buy/activation/{REGIONS.get_code(self.region, self.NAME)}/{self.operator}/whatsapp",
                    headers={
                        "Authorization": 'Bearer ' + KeyActivator.FIVE_SIM,
                        "Accept": "application/json"
                    },
                    timeout=2
                )
            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if response.status_code == 200 and response.text == "no free phones":
                if datetime.datetime.now() >= future:
                    raise activate_exceptions.GetNumberTimeoutException(Exception)

                time.sleep(1)

                continue

            if response.status_code == 400:
                raise activate_exceptions.BuyNumberException(response.text)

            break

        id = response.json().get("id")

        phone = str(response.json().get("phone")).replace("+", "")
        len_code = len(str(REGIONS.get_country_code(self.region)))
        code = phone[:len_code]
        phone = phone[len_code:]
        return id, code, phone

    def get_code(self, id: int, timeout=60):
        future = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

        while True:
            response = requests.get(
                url="https://5sim.net/v1/user/check/" + str(id),
                headers={
                    "Authorization": 'Bearer ' + KeyActivator.FIVE_SIM,
                    "Accept": "application/json"
                }

            )

            error = response.json().get("error")

            if error:
                raise activate_exceptions.GetActivationCodeException(response.text)

            sms = response.json().get("sms")
            if sms:
                code = sms[0].get("code")

            if not sms or code is None:

                if datetime.datetime.now() >= future:
                    raise activate_exceptions.TimeOutExceptionWaitCode(Exception)

                time.sleep(1)

                continue

            break

        return code

    def phone_confirm(self, id: int): ...

    def sms_confirm(self, id: int): ...

    def phone_cancel(self, id: int):
        self._update_number_status(id, status='cancel')
        return True

    def phone_ban(self, id: int):
        self._update_number_status(id, status='ban')
        return True

    def _update_number_status(self, id: int, status):
        response = requests.get(
            url=f"https://5sim.net/v1/user/{status}/" + str(id),
            headers={
                "Authorization": 'Bearer ' + KeyActivator.FIVE_SIM,
                "Accept": "application/json"
            }

        )
        if response.status_code >= 400:
            raise activate_exceptions.UpdateNumberStatusException(response.text)

        return response.text

    @classmethod
    def check_balance(self): ...
