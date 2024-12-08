import uiautomator2 as u2

from services import utils
from services.telephony import clear_sms


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        print(serial)
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        clear_sms(d)
        d.app_start('com.samsung.android.messaging')
