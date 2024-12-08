import os
import subprocess

import uiautomator2 as u2

import config
from services.props.other_props import prorp_generator, propsconf_late_template, manager


PROP_FILE = 'propsconf_late'
PROP_FILES_PATH = 'services/props/files'
MAGISK_PROP_CONF_PATH = '/data/adb/mhpc/propsconf_late'


def change_props(device: u2.Device, new_props=None):
    if new_props is None:
        prop_model = manager.get_random_props()
        new_props = prorp_generator.gen_props_list(prop_model)
    props_file = write_props_to_file(device, new_props)
    push_and_set_props(device, props_file)
    subprocess.run(f'adb -s {device.serial} reboot', shell=True)
    subprocess.run(f'adb -s {device.serial} wait-for-device ', shell=True)
    if new_props: return prop_model.id


def write_props_to_file(device: u2.Device, new_props: tuple[str], file_path: str = PROP_FILES_PATH):
    with open(f'{file_path}/{PROP_FILE}_{device.serial}', "w+") as file_to:
        file_to.write(propsconf_late_template.TEMPLATE.format(' '.join(new_props)))
    return f'{file_path}/{PROP_FILE}_{device.serial}'


def push_and_set_props(device: u2.Device, file_path: str) -> None:
    device.push(file_path, f'{config.PHONE_TMP_FOLDER}/{PROP_FILE}')
    device.shell(f"su -c 'cp {config.PHONE_TMP_FOLDER}/{PROP_FILE} {MAGISK_PROP_CONF_PATH}'")
    os.remove(file_path)
