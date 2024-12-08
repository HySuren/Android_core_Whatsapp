from services import utils
from services.contacts import contacts_manager
import time
import random


class ContactsUpdateException(Exception):
    def __init__(self, text=''):
        self.txt = text


def randomize(d, count=100):
    contacts_manager.clear_contacts_adb(d)
    contacts = []
    for _ in range(count):
        phone = '7' + random.choice(['911', '913', '914', '915', '916', '917', '918', '905', '903', '906', '909', '960', '964']) + str(random.randint(1000000, 9999999))
        contacts.append({'phone': phone})

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
            raise ContactsUpdateException
    if display.get('content-desc', 'Phone. Not selected').exists:
        d(description="Phone. Not selected").click()
        time.sleep(1)
        display = utils.get_display(d)
    if display.get('resource-id', 'android:id/button1').exists:
        d(resourceId="android:id/button1").click()
    d.keyevent('home')


def add_from_list(d, list):
    contacts_manager.clear_contacts_adb(d)
    contacts_manager.add(list, d)
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
            raise ContactsUpdateException
    if display.get('content-desc', 'Phone. Not selected').exists:
        d(description="Phone. Not selected").click()
        time.sleep(1)
        display = utils.get_display(d)
    if display.get('resource-id', 'android:id/button1').exists:
        d(resourceId="android:id/button1").click()
    d.keyevent('home')
