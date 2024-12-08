from services import utils
import subprocess


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        subprocess.call(f"adb -s {serial} reboot", shell=True, stdout=subprocess.DEVNULL)
