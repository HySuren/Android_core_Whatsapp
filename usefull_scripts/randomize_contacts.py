import uiautomator2 as u2
from services import utils
from services.contacts import contacts_manager
import time
import random


def run():
    devices_serials = utils.get_list_adb()
    for serial in devices_serials[0]:
        print(serial)
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')

        contacts_manager.clear_contacts_adb(d)
        contacts = []
        for i in range(100):
            contacts.append({'phone': str(random.randint(79000000000, 79999999999))})
        contacts_manager.add(contacts, d)
        time.sleep(2)
        display = utils.get_display(d)
        if display.get('resource-id', 'com.android.permissioncontroller:id/permission_allow_button').exists:
            d(resourceId='com.android.permissioncontroller:id/permission_allow_button').click()
            time.sleep(5)
            display = utils.get_display(d)

        if display.get('resource-id', 'com.samsung.android.app.contacts:id/menu_done').exists:
            d(resourceId='com.samsung.android.app.contacts:id/menu_done').click()
            time.sleep(1)
            display = utils.get_display(d)
        else:
            time.sleep(5)
            display = utils.get_display(d)
            if display.get('resource-id', 'com.samsung.android.app.contacts:id/menu_done').exists:
                d(resourceId='com.samsung.android.app.contacts:id/menu_done').click()
                time.sleep(1)
                display = utils.get_display(d)
            else:
                raise Exception(f'{serial} ахуевший')
        if display.get('content-desc', 'Phone. Not selected').exists:
            d(description="Phone. Not selected").click()
            time.sleep(1)
            display = utils.get_display(d)
        if display.get('resource-id', 'android:id/button1').exists:
            d(resourceId="android:id/button1").click()

        d.screen_off()
