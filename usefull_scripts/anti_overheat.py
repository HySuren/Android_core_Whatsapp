import uiautomator2 as u2
from services import utils
import time


def run():
    n_devices, n_bad_devices = utils.get_list_adb()

    for serial in n_devices:
        print(f'Connected to {serial}')
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        while utils.get_display(d).get('package', 'com.sec.android.sdhms').exists:
            d(resourceId="android:id/button1").click()
            print('Frame sdhms closed!')
            time.sleep(1)
        d.app_stop("com.android.chrome")
        d.shell("pm clear com.android.chrome")
        print('Chrome stopped!')
