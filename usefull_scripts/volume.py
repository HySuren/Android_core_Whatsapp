import uiautomator2 as u2
from services import utils
from scrip_iterations_rules import phone_preparation


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        print(serial)
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        d.shell(f'cmd notification set_dnd off')
        for i in (1, 2, 3, 4, 5, 6):
            d.shell(f'cmd media_session volume --stream {i} --set 15')
        phone_preparation.turn_airplane_mode(d, on=False)
        d.screen_off()
