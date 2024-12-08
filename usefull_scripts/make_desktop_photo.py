import re
import subprocess
import time

from PIL import Image, ImageDraw, ImageFont
import psycopg2
import uiautomator2 as u2

DEVICE_PAIRS = {'RZ8RB1MHR9J': 'HZQL1838HAKB1302949', 'RZ8RB1MHD4X': 'HZQL1838HAKA2901891', 'RF8RA1AATWY': 'HZQL1838HAKA3000391', 'RZ8RB1F2DTZ': 'HZQL1838HAKB0400313', 'RZ8RB0P38PT': 'HZQL1838HAKA3002450', 'RZ8RB0P38GH': 'HZQL1838HAKA3001185', 'RF8RA0TRXWK': 'HZQL1838HAKB1302631', 'RF8T11BW5MA': 'HZQL1838HAKA3002345', 'RF8RB0CXHRN': 'HZQL1838HAKA2901260', 'RF8RB1B15JX': 'HZQL1838HAKB1303006', 'RF8RA0T3WZN': 'HZQL1838HAKA3000177', 'RF8RC0J8J6Y': 'RF8R806APML', 'RF8T11BW3QK': 'FS0CXM101513', 'RZ8RB1MHYBZ': '320106648726', 'RF8T11BYSSB': 'R58R82YG62X', 'RZ8RB1F2HBV': 'FS14EM102262', 'RF8RA1AAN8A': 'RF8R80ADR3A', 'RZ8RB1K37PH': '320207317750', 'RF8T11BX1BL': '320207315315', 'RF8RB1B0HZX': 'RF8RB00J0HL', 'RF8RC0J9KDT': 'RZ8RB1MHBZE', 'RF8RC0BTM6H': 'RZ8RB1K4V7W', 'RZ8RB1EY1MF': 'RZ8RB0P399L', 'RF8RB1AZDVZ': '320106648770'}


def connectPg():
    conn = psycopg2.connect(host='wa3.qeepmail.ru', port='5432', dbname='whatsapp_dev', user='wa_dev', password='KvakvaparkturandontihatewaiteTUdICTOR')
    curs = conn.cursor()
    return conn, curs


def disconnectPg(conn, curs):
    curs.close()
    conn.close()


def set_wallpaper(serials_with_ids, adb):
    for device in serials_with_ids.keys():
        if device not in adb:
            continue
        phone = u2.connect(device)
        if subprocess.run(['adb', '-s', f'{device}', 'shell', 'dumpsys', 'power', '|', 'grep', '"Display Power"'], check=True, capture_output=True, text=True).stdout.replace('\n', '') == 'Display Power: state=OFF':
            subprocess.call(f"adb -s {device} shell input keyevent 26", shell=True, stdout=subprocess.DEVNULL)
        phone.keyevent('home')
        generate_image(serial=device, id=serials_with_ids[device])
        subprocess.call(f"adb -s {device} push result.png /sdcard/", shell=True, stdout=subprocess.DEVNULL)
        subprocess.call(f"adb -s {device} shell am start \
            -a android.intent.action.ATTACH_DATA \
            -c android.intent.category.DEFAULT \
            -d file:///sdcard/result.png \
            -t 'image/*' \
            -e mimeType 'image/*'", shell=True, stdout=subprocess.DEVNULL)

        time.sleep(1)
        subprocess.call(f"adb -s {device} shell input tap 617 1084", shell=True, stdout=subprocess.DEVNULL)

        subprocess.call(f"adb -s {device} shell input tap 192 1471", shell=True, stdout=subprocess.DEVNULL)

        time.sleep(2)
        subprocess.call(f"adb -s {device} shell input tap 350 1450", shell=True, stdout=subprocess.DEVNULL)

        subprocess.call(f"adb -s {device} shell input keyevent KEYCODE_HOME", shell=True, stdout=subprocess.DEVNULL)


def generate_image(serial, id):
    width = 720
    height = 1560

    serial = f"serial: {serial}"
    id = f"id: {id}"

    font = ImageFont.truetype("impact2.ttf", size=80)
    font2 = ImageFont.truetype("impact2.ttf", size=140)

    img = Image.new('RGB', (width, height), color='white')

    imgDraw = ImageDraw.Draw(img)

    textWidth, textHeight = imgDraw.textsize(serial, font=font)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2

    imgDraw.text((xText, yText), serial, font=font, fill=(0, 0, 0))

    textWidth, textHeight = imgDraw.textsize(id, font=font2)
    xText = (width - textWidth) / 2
    yText = (height - textHeight) / 2 + 80

    imgDraw.text((xText, yText), id, font=font2, fill=(0, 0, 0))

    img.save('result.png')


def get_list_adb(all=False):
    devices = []
    bad_devices = []
    out = subprocess.run(['adb', 'devices'], check=True, capture_output=True, text=True).stdout.split('\n')
    for line in out:
        regex = re.split(r'\t', line)
        if len(regex) == 2:
            if regex[1] == 'device' and (all or (len(regex[0]) == 11 and regex[0] not in DEVICE_PAIRS.values())):
                devices.append(regex[0])
            else:
                bad_devices.append(regex[0])
    return devices, bad_devices


def make_devices():
    devices = dict()
    select = f"select serial, id from  devices;"
    conn, curs = connectPg()
    curs.execute(select)
    rows = curs.fetchall()
    for row in rows:
        devices[row[0]] = row[1]
    disconnectPg(conn, curs)
    return devices


if __name__ == '__main__':
    good, bad = get_list_adb()
    devices = make_devices()
    set_wallpaper(devices, good)
