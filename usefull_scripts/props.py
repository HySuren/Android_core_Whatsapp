import random
import subprocess
import time
from threading import Thread

import uiautomator2 as u2

from services import utils
from services.props.other_props.manager import get_props_id_by_fingerprint, update_device_prop


def change(serial):
    with subprocess.Popen(f'adb -s {serial} shell props -nw', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          universal_newlines=True, bufsize=1) as cat:
        commands = ['1', 'f', str(random.randint(1, 32)), '{randomlen}', '{chversions}', 'y', 'n', 'b', 'b', 'b', '3',
                    's', 'y', '1,2,3,9,10', '1', 'y']
        while True:
            menu = ''
            while True:
                output = cat.stdout.read(1)
                menu += output
                if 'Enter your desired option: ' in menu or 'Enter y(es), n(o) or e(xit): ' in menu:
                    break
            command = commands.pop(0)
            if command == '{chversions}':
                if 'There are several fingerprints available' in menu:
                    command = '1'
                    commands = commands[:3] + ['b'] + commands[3:]
                else:
                    command = commands.pop(0)
            if 'Device simulation (enabled)' in menu and command == 's':
                commands.pop(0)
                command = commands.pop(0)
            if command == '{randomlen}':
                num = menu.split('1 - ')[1].split('\nb - ')[0].split('\n')[-1].split(' - ')[0]
                num = 1 if len(num) > 3 else num
                command = str(random.randint(1, int(num)))
            print(command, file=cat.stdin, flush=True)
            if len(commands) == 0:
                break


def reset(serial):
    with subprocess.Popen(f'adb -s {serial} shell props -nw', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          universal_newlines=True, bufsize=1) as cat:
        commands = ['1', 'r', 'y', 'y']
        while True:
            menu = ''
            while True:
                output = cat.stdout.read(1)
                menu += output
                if 'Enter your desired option: ' in menu or 'Enter y(es), n(o) or e(xit): ' in menu:
                    break
            command = commands.pop(0)
            if command == '{chversions}':
                if 'There are several fingerprints available' in menu:
                    command = '1'
                    commands = commands[:3] + ['b'] + commands[3:]
                else:
                    command = commands.pop(0)
            if 'Device simulation (enabled)' in menu and command == 's':
                commands.pop(0)
                command = commands.pop(0)
            if command == '{randomlen}':
                num = menu.split('1 - ')[1].split('\nb - ')[0].split('\n')[-1].split(' - ')[0]
                num = 1 if len(num) > 3 else num
                command = str(random.randint(1, int(num)))
            print(command, file=cat.stdin, flush=True)
            if len(commands) == 0:
                break


def change_props():
    n_devices, n_bad_devices = utils.get_list_adb()

    for serial in n_devices:
        Thread(target=change, args=(serial,)).start()


def rollback_props():
    n_devices, n_bad_devices = utils.get_list_adb()

    for serial in n_devices:
        Thread(target=reset, args=(serial, )).start()


def enable_props():
    n_devices, n_bad_devices = utils.get_list_adb()

    for serial in n_devices:
        print(f'Connected to {serial}')
        d = u2.connect(serial)
        d.screen_on()
        d.keyevent('home')
        d.app_stop('com.topjohnwu.magisk')
        d.app_start('com.topjohnwu.magisk')
        tries = 3
        while not utils.get_display(d).get('content-desc', 'Modules').exists and tries > 0:
            time.sleep(1)
            tries -= 1
        if tries == 0:
            print('bad phone')
            continue
        d(description="Modules").click()
        try:
            d(resourceId="com.topjohnwu.magisk:id/0_resource_name_obfuscated", text="OFF").click()
        except:
            ...
        d.keyevent('home')
        d.screen_off()


def get_props():
    n_devices, n_bad_devices = utils.get_list_adb()
    for serial in n_devices:
        d = u2.connect(serial)
        finger_from_shell = d.shell('getprop |grep finger').output
        finger = finger_from_shell.split('\n')[0].split(']: [')[1].replace(']', '')
        update_device_prop(finger, serial)
        prop_id = get_props_id_by_fingerprint(finger)
        print(prop_id, d.serial, finger)


def install():
    n_devices, n_bad_devices = utils.get_list_adb()
    for serial in n_devices:
        print(f'Connected to {serial}')
        d = u2.connect(serial)
        d.push('./services/MagiskHidePropsConfig-v6.1.2.zip',
               './storage/emulated/0/Download/MagiskHidePropsConfig-v6.1.2.zip')
        d.screen_on()
        d.keyevent('home')
        d.app_stop('jsnyw.jz')
        d(description='Settings').click()
        tries = 10
        while not utils.get_display(d).get('content-desc', 'Modules').exists and tries > 0:
            time.sleep(1)
            tries -= 1
        if tries == 0:
            print('bad phone')
            continue
        d(description="Modules").click()
        if not utils.get_display(d).get('text', 'MagiskHide Props Config').exists:
            d(text="Install from storage").click()
            while not utils.get_display(d).get('text', 'This week').exists:
                time.sleep(1)
            d(text="This week").click()
            time.sleep(2)
            d(resourceId="com.google.android.documentsui:id/item_root").click()
            while not utils.get_display(d).get('text', 'Reboot').exists:
                time.sleep(1)
            d(resourceId="com.topjohnwu.magisk:id/restart_btn").click()
        else:
            d.keyevent('home')
            d.screen_off()
