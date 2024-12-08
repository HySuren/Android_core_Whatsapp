import uiautomator2 as u2

import config
from . import conf


def install_sqllite(device: u2.Device):
    device.push(f'{conf.PATH_TO_FILES}/sqlite3', f'{config.PHONE_TMP_FOLDER}/')
    device.push(f'{conf.PATH_TO_FILES}/sql_query', f'{config.PHONE_TMP_FOLDER}/')
    device.shell(f'su -c cp {config.PHONE_TMP_FOLDER}/sqlite3 /system/bin/')
    device.shell('su -c chmod 775 /system/bin/sqlite3')


def request_to_wa_database(device: u2.Device, sql_query: str):
    wa_db_path = '/data/data/com.whatsapp/databases/wa.db'
    try:
        output = device.shell(fr'sh {config.PHONE_TMP_FOLDER}/sql_query "{sql_query}" {wa_db_path}').output
        return output.decode('utf-8')
    except:
        ...


def get_contacts(device: u2.Device) -> list[str]:
    item = request_to_wa_database(device, "select number  from wa_contacts where is_whatsapp_user = 1;")
    if item:
        return item.strip().split()
    return []


def clear_contacts(device: u2.Device) -> None:
    request_to_wa_database(device, "DELETE FROM wa_contacts WHERE jid != 'status@broadcast';")


