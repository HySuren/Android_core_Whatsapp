import uiautomator2 as u2

from services import utils
from concurrent.futures import ThreadPoolExecutor


def disable_adb_timeout(serial: str) -> None:
    try:
        d = u2.connect(serial)
        d.press('home')
        d.press('home')
        d.app_stop('com.android.settings')
        d.app_start('com.android.settings')
        for _ in range(7):
            d.swipe_ext("up", 1)
        d(resourceId="android:id/title", text="Developer options").click()
        d.swipe_ext("down", 3)
        for _ in range(2):
            d.swipe_ext("up", 1)

        o = d.xpath('//*[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[7]/android.widget.LinearLayout[1]/android.widget.Switch[1]')
        if o.get_text() == 'Off':
            d.xpath('//*[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[7]/android.widget.LinearLayout[1]/android.widget.Switch[1]').click()
    except Exception as e:
        print(f'Exception by {serial} - {e}')


def multi_thread_disable():
    devices, _ = utils.get_list_adb(all=True)
    with ThreadPoolExecutor() as executor:
        executor.map(disable_adb_timeout, devices)


def run():
    multi_thread_disable()


if __name__ == '__main__':
    multi_thread_disable()
