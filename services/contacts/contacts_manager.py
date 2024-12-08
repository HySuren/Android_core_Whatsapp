import os

import uiautomator2 as u2

import config
from services import utils
from . import sqllite, conf


def clear(device: u2.Device) -> None:
    # sqllite.install_sqllite(device)
    clear_contacts_adb(device)
    # sqllite.clear_contacts(device)


def add(phones: list[dict], device: u2.Device) -> None:
    # sqllite.install_sqllite(device)
    gen_vcard(phones, device.serial)
    add_contact_adb(device)


def check(phones: list[str], device: u2.Device) -> tuple[list[str], list[str]]:
    added_contacts = utils.clen_numbers(sqllite.get_contacts(device))
    not_added_contacts = list(set(phones) - set(added_contacts))
    return added_contacts, not_added_contacts


# SERVICES

def clear_contacts_adb(device: u2.Device):
    # device.shell("am force-stop com.google.android.packageinstaller")
    device.shell("pm clear com.samsung.android.providers.contacts")
    device.shell("pm clear com.android.providers.contacts")


def gen_vcard(numbers, serial):
    with open(f'{conf.PATH_TO_FILES}/contacts-{serial}.vcf', 'w') as vcf_file:
        text_vcard = ''
        for number in numbers:
            if number.get('name'):
                text_vcard += f'BEGIN:VCARD\nVERSION:3.0\nN:{number["name"]};;;;\nTEL;TYPE=cell:+{number["phone"]}\nEND:VCARD\n'
            else:
                text_vcard += f'BEGIN:VCARD\nVERSION:3.0\nN:{"+"+str(number["phone"])};;;;\nTEL;TYPE=cell:+{number["phone"]}\nEND:VCARD\n'
        vcf_file.write(text_vcard)


def add_contact_adb(device: u2.Device):
    # clear_contacts_adb(device)
    device.push(f'{conf.PATH_TO_FILES}/contacts-{device.serial}.vcf', f'{config.PHONE_TMP_FOLDER}/contacts.vcf')

    for contact_app in ('com.android.contacts', 'com.google.android.contacts', 'com.samsung.android.app.contacts'):
        device.shell(f'am start -t "text/vcard" -d "file:///{config.PHONE_TMP_FOLDER}/contacts.vcf" -a android.intent.action.VIEW {contact_app}')
    os.remove(f'{conf.PATH_TO_FILES}/contacts-{device.serial}.vcf')


def press_to_import(device: u2.Device):
    device.xpath('//*[@resource-id="com.samsung.android.app.contacts:id/menu_done"]/android.view.ViewGroup[1]').click()
