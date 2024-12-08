import base64
from io import BytesIO
import os
import subprocess

from PIL import Image, ImageOps
import requests

import config


class BackupServiceException(Exception):
    def __init__(self, text=''):
        self.txt = text


class BackupExistsException(BackupServiceException):
    ...


class BackupService:
    def __init__(self, serial, backup_name, pairs):
        self.serial = serial
        self.serial_qr = pairs[serial]
        self.backup_name = backup_name

    def create_web_backup(self):

        response = requests.request("POST", f"{config.WEB_API_DOMAIN}/new", params={"name": self.backup_name})
        if response.status_code == 200:
            qr = response.text
            with Image.open(BytesIO(base64.b64decode(qr.replace('data:image/png;base64,', '')))) as image:
                image.save(f'{self.backup_name}_code.png')
            with Image.open(f'{self.backup_name}_code.png') as image:
                ImageOps.expand(image, border=80, fill='white').save(f'{self.backup_name}_code.png')
            subprocess.call(f"adb -s {self.serial_qr} push {self.backup_name}_code.png /storage/emulated/0/DCIM/Camera/", shell=True, stdout=subprocess.DEVNULL)
            os.remove(f'{self.backup_name}_code.png')
            subprocess.call(f"adb -s {self.serial_qr} shell settings put system screen_brightness 250", shell=True, stdout=subprocess.DEVNULL)
            subprocess.call(f"adb -s {self.serial_qr} shell settings put system screen_brightness_mode 0", shell=True, stdout=subprocess.DEVNULL)
            subprocess.call(f"adb -s {self.serial_qr} shell am force-stop com.google.android.apps.photos", shell=True, stdout=subprocess.DEVNULL)
            subprocess.call(f"adb -s {self.serial_qr} shell am start -d file:///storage/emulated/0/DCIM/Camera/{self.backup_name}_code.png -t image/jpg -a android.intent.action.VIEW", shell=True, stdout=subprocess.DEVNULL)
            if subprocess.run(['adb', '-s', f'{self.serial_qr}', 'shell', 'dumpsys', 'power', '|', 'grep', '"Display Power"'], check=True, capture_output=True, text=True).stdout.replace('\n', '') == 'Display Power: state=OFF':
                subprocess.call(f"adb -s {self.serial_qr} shell input keyevent 26", shell=True, stdout=subprocess.DEVNULL)
        else:
            print(response.text)
            if 'Backup exists' in response.text:
                raise BackupExistsException
            else:
                raise BackupServiceException

    def delete_web_backup(self):
        requests.request("DELETE", f"{config.WEB_API_DOMAIN}/backup/{self.backup_name}")

    def close_session(self):
        requests.request("POST", f"{config.WEB_API_DOMAIN}/{self.backup_name}/close")

    def check_backup_exists(self):
        response = requests.request("GET", f"{config.WEB_API_DOMAIN}/backup/{self.backup_name}/exists")
        if response.status_code == 200:
            return response.json()
        else:
            raise BackupServiceException

    def finish(self):
        subprocess.call(f"adb -s {self.serial_qr} shell am force-stop com.google.android.apps.photos", shell=True, stdout=subprocess.DEVNULL)
        subprocess.call(f"adb -s {self.serial_qr} shell rm -f /storage/emulated/0/DCIM/Camera/*", shell=True, stdout=subprocess.DEVNULL)
        if subprocess.run(['adb', '-s', f'{self.serial_qr}', 'shell', 'dumpsys', 'power', '|', 'grep', '"Display Power"'], check=True, capture_output=True, text=True).stdout.replace('\n', '') == 'Display Power: state=ON':
            subprocess.call(f"adb -s {self.serial_qr} shell input keyevent 26", shell=True, stdout=subprocess.DEVNULL)
