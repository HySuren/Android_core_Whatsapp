import os
import random

import requests
import uiautomator2 as u2

import config

SAVE_LINK_PHONE = f'{config.PHONE_TMP_FOLDER}/image_files/'

SAVE_IMG_PATH = os.getcwd() + '/services/photos'
PHONE_IMAGES_FOLDER = '/storage/emulated/0/DCIM/Camera/'


def get_and_save_random_on_photo(device: u2.Device, cdn=config.CDN, change_size=False, set_blur=False, put_text=False, count=1):
    # get random photo from cdn
    cdn_folder = cdn.folder_file_list('test')
    file_names = [random.choice(cdn_folder) for _ in range(count)]
    for i in file_names:
        file_name = i
        # download it
        cdn.download_file(file_name, SAVE_IMG_PATH, 'test/womans')
        # randomize
        # img = ImageRandomizer(f'{SAVE_IMG_PATH}/{file_name}')
        # if change_size: img = img.size()
        # if set_blur: img = img.blur()
        # if put_text: img = img.text()
        # img.save()

        device.push(f'{SAVE_IMG_PATH}/{file_name}', PHONE_IMAGES_FOLDER)
        # index this photo (need to view img in gallery)
        device.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{PHONE_IMAGES_FOLDER}/{file_name}')
        # remove photo on pc
        os.remove(f'{SAVE_IMG_PATH}/{file_name}')
    return file_names[-1]


def remove_all_photos(device: u2.Device):
    f = device.shell(f"ls {PHONE_IMAGES_FOLDER}")
    files = f.output.split('\n')[:-1]
    for file in files:
        remove_photo(device, file)


def remove_photo(device: u2.Device, file_name):
    device.shell(f'rm {PHONE_IMAGES_FOLDER}/{file_name}')


def get_and_save_skillbox_on_photo(device: u2.Device, cdn=config.CDN, change_size=False, set_blur=False, put_text=False, count=1):
    # get random photo from cdn
    cdn_folder = cdn.folder_file_list('skillbox_womans')
    file_names = [random.choice(cdn_folder) for _ in range(count)]
    for i in file_names:
        file_name = i
        # download it
        cdn.download_file(file_name, SAVE_IMG_PATH, 'skillbox_womans/womans')
        # randomize
        # img = ImageRandomizer(f'{SAVE_IMG_PATH}/{file_name}')
        # if change_size: img = img.size()
        # if set_blur: img = img.blur()
        # if put_text: img = img.text()
        # img.save()

        device.push(f'{SAVE_IMG_PATH}/{file_name}', PHONE_IMAGES_FOLDER)
        # index this photo (need to view img in gallery)
        device.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{PHONE_IMAGES_FOLDER}/{file_name}')
        # remove photo on pc
        os.remove(f'{SAVE_IMG_PATH}/{file_name}')
    return file_names[-1]


def get_and_save_generated_photo(device: u2.Device, photo_url):
    file_name = f'mixed_{device.serial}.jpg'
    file_path = f'{SAVE_IMG_PATH}/{file_name}'
    img_data = requests.get(photo_url).content
    with open(file_path, 'wb') as handler:
        handler.write(img_data)
    device.push(file_path, PHONE_IMAGES_FOLDER)
    device.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///{PHONE_IMAGES_FOLDER}/{file_name}')
    os.remove(file_path)
    return 'mixed_photo'
