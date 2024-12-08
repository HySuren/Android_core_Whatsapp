import subprocess
import config
import uiautomator2 as u2
from concurrent.futures import ThreadPoolExecutor

from services import utils


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        print(serial)
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        d.shell("pm uninstall com.whatsapp")
        subprocess.call(f"adb -s {serial} install -d ./apk/{config.WA_VERSION}.apk", shell=True, stdout=subprocess.DEVNULL)
        d.shell('su -c "magisk --denylist add com.whatsapp"')
        d.shell("pm clear com.whatsapp")
        d.screen_off()


def reinstall_wa(serial: str) -> None:
    try:
        print(f'Starting reinstall wa for {serial}')
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        d.shell("pm uninstall com.whatsapp")
        subprocess.call(f"adb -s {serial} install -d ./apk/{config.WA_VERSION}.apk", shell=True, stdout=subprocess.DEVNULL)
        d.shell('su -c "magisk --denylist add com.whatsapp"')
        d.shell("pm clear com.whatsapp")
        d.screen_off()
        print(f'Finished reinstall wa for {serial}')
    except Exception as e:
        print(f'Exception by {serial} - {e}')


def multi_restart_wa():
    devices, _ = utils.get_list_adb(all=True)
    with ThreadPoolExecutor() as executor:
        executor.map(reinstall_wa, devices)


def run():
    multi_restart_wa()


if __name__ == '__main__':
    multi_restart_wa()
