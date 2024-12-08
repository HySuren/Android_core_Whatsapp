import uiautomator2 as u2
from services import utils


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        print(serial)
        d = u2.connect(serial)
        contacts_raw = d.shell("content query --uri content://com.android.contacts/contacts --projection display_name")
        contacts = list(filter(lambda a: a != '', ['='.join(n.split('=')[1:]) for n in contacts_raw.output.split('\n')]))
        print(len(contacts))
