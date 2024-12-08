from services.backup.create import backup, tardir
from services import utils


def backup_locally():

    devices, _ = utils.get_list_adb()
    for serial in devices:
        backup(serial, serial, 'com.whatsapp')
        tardir(serial)
