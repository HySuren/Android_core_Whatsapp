import uiautomator2 as u2

from services import utils


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        print(serial)
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        d.shell("pm uninstall org.sandroproxy.drony")
        d.screen_off()
