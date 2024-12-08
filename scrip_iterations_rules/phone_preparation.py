import logging
import time

from requests import ReadTimeout, RequestException
import uiautomator2 as u2

import core.exceptions


# TODO (Misha)
#   вкл:
#       * не беспокоить                             +-
#       * мобильный интернет                        ✅
#       * английский язык интерфейса                +-
#       * shell в magisk
#       * время активности экрана - 30 минут        ✅
#       * экран блокировки:                         ✅
#   выкл:                                           __
#       * поворот экрана                            ✅
#       * вайфай                                    ✅
#   _                                               __
#   - узнать оператора                              ?
#   - узнать номер                                  ?
#   - узнать баланс                                 ?
#   - проверить ip и интернет (без браузера)        ✅


def turn_off_wifi(device: u2.Device):
    device.shell('svc wifi disable')


def turn_internet(device: u2.Device, on=True):
    device.shell(f'svc data {"enable" if on else "disable"}')


def turn_off_accelerometer_rotation(device: u2.Device):
    device.set_orientation(0)
    device.shell('settings put system accelerometer_rotation 0')


def set_screen_timeout(device: u2.Device, timeout=1800000):
    device.shell(f'settings put system screen_off_timeout {timeout}')


def disable_lockscreen_swipe(device: u2.Device):
    device.shell('locksettings set-disabled true')


def turn_airplane_mode(device: u2.Device, on=False, count=100):
    for _ in range(count):
        try:
            device.shell(f'settings put global airplane_mode_on {int(on)}')
            device.shell("su -c 'am broadcast -a android.intent.action.AIRPLANE_MODE'")
            break
        except Exception as e:
            if isinstance(e, RequestException):
                pass


def get_ip(device: u2.Device,  timout=3):
    try:
        if check_ping(device):
            return 'success'
    except ReadTimeout:
        return
    return


def check_ping(device: u2.Device) -> bool:
    answer = device.shell("echo 'GET /' | ping -c1 google.com").output.strip()
    if answer.find("1 received") != -1:
        if float(answer[answer.find("time=") + 5:].split(maxsplit=1)[0]) < 1500:
            return True
    return False


def check_internet(device, retries=25):
    for i in range(retries):
        ip = get_ip(device)
        logging.info(f'Вот какой инет: {ip}, кол попыток {i}')
        if ip == 'success':
            return ip
        else:
            time.sleep(0.5)
    raise core.exceptions.NoInternetException


def change_ip(device: u2.Device):
    turn_airplane_mode(device, on=True)
    time.sleep(1)
    turn_airplane_mode(device, on=False)
    ip = check_internet(device)
    return ip
