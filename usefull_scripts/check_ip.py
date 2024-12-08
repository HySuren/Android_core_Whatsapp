import uiautomator2 as u2
from services import utils
from scrip_iterations_rules import phone_preparation
from core.exceptions import NoInternetException


def run():
    for serial in utils.get_list_adb()[0]:
        d = u2.connect(serial)
        phone_preparation.turn_airplane_mode(d, on=False)
        phone_preparation.turn_off_wifi(d)
        phone_preparation.turn_internet(d, on=True)
        try:
            ip = phone_preparation.check_internet(d)
            print(f'{serial} - {ip}')
        except NoInternetException:
            print(f'{serial} - no internet')
