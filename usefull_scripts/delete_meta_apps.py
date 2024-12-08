import uiautomator2 as u2
from services import utils


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        d = u2.connect(serial)
        packages = ['com.spotify.music', 'com.facebook.katana']
        for package in packages:
            d.shell(f"pm uninstall {package}")
