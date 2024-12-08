import time
import datetime
import requests

from .config import KeyActivator, ActivatorName, ActivatorTimeout, REGIONS
from .base_activator import BaseActivator
from . import activate_exceptions


class SmsActivate(BaseActivator):

    NAME = ActivatorName.SMS_ACTIVATE

    def get_phone(self, obj, srvice='wa', free_price=False, max_free_price=None, free_price_array=None):
        global response
        future = datetime.datetime.now() + datetime.timedelta(seconds=ActivatorTimeout.GET_NUMBER_SECONDS)
        obj.logger.info(f'starting get_phone')
        if REGIONS.get_code(self.region, self.NAME) != '0':
            self.operator = 'any'

        while True:
            try:
                if free_price and len(free_price_array) > 0:
                    for price in free_price_array:
                        obj.logger.info(f'price: {price}')
                        response = self._request_phone(srvice='wa', free_price=free_price, price=price, obj=obj)

                        obj.logger.info(f'request end with {response.status_code} status_code: {response.text}')
                        if '{' in response.text and response.json().get('activationId'):
                            break
                        time.sleep(3)
                elif free_price and max_free_price:
                    response = self._request_phone(srvice='wa', free_price=free_price, price=max_free_price, obj=obj)
                    obj.logger.info(f'request end with {response.status_code} status_code: {response.text}')
                else:
                    response = requests.post(
                        url="https://sms-activate.org/stubs/handler_api.php?",
                        params={
                            "api_key": KeyActivator.SMS_ACTIVATE,
                            "action": "getNumberV2",
                            "service": srvice,
                            "country": REGIONS.get_code(self.region, self.NAME),
                            "operator": self.operator
                        },
                    )
                    obj.logger.info(f'request end with {response.status_code} status_code: {response.text}')

            except Exception as e:
                if isinstance(e, requests.exceptions.RequestException):
                    raise activate_exceptions.PhoneActivationException(Exception)
                else:
                    raise e

            if '{' in response.text and response.json().get('activationId'):
                break

            if datetime.datetime.now() >= future:
                raise activate_exceptions.GetNumberTimeoutException(Exception)

            time.sleep(3)

            if obj.sms_activate_response_enable:
                if response.status_code >= 500:
                    obj.device_info.params['sms_activate_response']['responses'].append({"status_code": response.status_code, "response_text": "HTML_ERROR", 'service': 'sms_activate'})
                else:
                    obj.device_info.params['sms_activate_response']['responses'].append({"status_code": response.status_code, "response_text": response.text, 'service': 'sms_activate'})

            # TODO Посмотреть из логов какая ошибка приходит в json
            if "no_balance" in response.text.lower() or "whatsapp_not_available" in response.text.lower():
                raise activate_exceptions.BuyNumberException(Exception)
            elif 'banned' in response.text.lower():
                raise activate_exceptions.BanException(Exception)

        if obj.sms_activate_response_enable:
            obj.logger.info(f'logging sms_activate answer')
            # Может прийти NO_NUMBERS - не json
            try:
                phone, price = response.json().get('phoneNumber'), response.json().get('activationCost')
                obj.device_info.params['sms_activate_response']['prices'].append({phone: price})
            except Exception as e:
                if isinstance(e, requests.exceptions.JSONDecodeError):
                    obj.logger.info('response not valid json')
                else:
                    raise e

        id, phone = response.json().get('activationId'), response.json().get('phoneNumber')

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
            url="https://sms-activate.org/stubs/handler_api.php?",
            params={
                "api_key": KeyActivator.SMS_ACTIVATE,
                "action": "setStatus",
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

    def _request_phone(self, srvice='wa', free_price=False, price=None, obj=None):
        response = requests.post(
            url="https://sms-activate.org/stubs/handler_api.php?",
            params={
                "api_key": KeyActivator.SMS_ACTIVATE,
                "action": "getNumberV2",
                "service": srvice,
                "country": REGIONS.get_code(self.region, self.NAME),
                "operator": self.operator,
                "freePrice": free_price,
                "maxPrice": price
            },
        )

        if obj.sms_activate_response_enable:
            if response.status_code >= 500:
                obj.device_info.params['sms_activate_response']['responses'].append({"status_code": response.status_code, "response_text": "HTML_ERROR", 'service': 'sms_activate'})
            else:
                obj.device_info.params['sms_activate_response']['responses'].append({"status_code": response.status_code, "response_text": response.text, 'service': 'sms_activate'})

        return response

