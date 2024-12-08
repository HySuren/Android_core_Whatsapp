import random
import subprocess


"""
    set_level(percent) устанавливает уровень заряда
    set_status(status) устанавливает статус зарядки (unknown, charging, discharging, not_charging, full)
    set_usb(usb) устанавливает статус usb (on, off)
    reset() возвращает реальные параметры батареи устройства
    change_battery(status, usb, percent) вызывает сразу все 4 предыдущие функции

    Параметры change_battery(status, usb, percent) по умолчакнию:
        * status = 'not_charging',
        * usb = 'off',
        * level = random.randint(20, 100)
"""


BATTERY_STATUSES_DICT = {
    'charging': 1,
    'discharging': 2,
    'not_charging': 3,
    'full': 4
}

BATTERY_USB_STATUSES_DICT = {
    'on': 0,
    'off': 1
}


def change_battery_random(serial):
    change_battery(serial,
        random.choice(list(BATTERY_USB_STATUSES_DICT.keys())),
        random.choice(list(BATTERY_STATUSES_DICT.keys())),
        (20, 100)
    )


def change_battery(serial, usb: str = 'off', status: str = 'not_charging', percents: tuple[int, int] = (10, 90)):
    reset(serial)
    set_usb(serial, usb=usb)
    set_status(serial, status=status)
    set_level(serial, percent=random.randint(*percents))


def set_level(serial, percent):
    assert not 0 > percent >= 100
    subprocess.run(f'adb -s {serial} shell dumpsys battery set level {percent}', shell=True)


def set_status(serial, status):
    assert BATTERY_STATUSES_DICT.get(status) is not None
    subprocess.run(f'adb -s {serial} shell dumpsys battery set status {BATTERY_STATUSES_DICT[status]}', shell=True)


def set_usb(serial, usb):
    assert BATTERY_USB_STATUSES_DICT.get(usb) is not None
    subprocess.run(f'adb -s {serial} shell dumpsys battery set usb {BATTERY_USB_STATUSES_DICT[usb]}', shell=True)


def reset(serial):
    subprocess.run(f'adb -s {serial} shell dumpsys battery reset', shell=True)
