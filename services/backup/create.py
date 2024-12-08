import os
import shutil
import subprocess
import tarfile
import uuid

from requests import RequestException

import config
from services.backup import conf


def create_dump(serial, app, cdn=config.CDN) -> str:
    sdn_uniq = str(uuid.uuid4())
    backup(serial, sdn_uniq, app)
    tardir(sdn_uniq)
    try:
        cdn.upload_file(sdn_uniq, conf.FILES_DIR, 'yandex/backups')
    except Exception as e:
        if isinstance(e, ConnectionError) or isinstance(e, RequestException):
            print(f'WARNING {cdn.__name__} CANT UPLOAD BACKUP WITH {sdn_uniq} KEY')
        else:
            raise e
    return sdn_uniq


def tardir(dump_name: str):
    """ Для архивации WA дампа.
    Принимает название дампа находящегося в files/dumps_WA_acc/
    УДАЛЯЕТ ПАПКУ С ДАМПОМ! """

    if dump_name not in os.listdir(conf.DUMP_DIR):
        raise FileExistsError(f'File {dump_name} not exists!')

    tar_path = f'{conf.FILES_DIR}/{dump_name}'
    dump_path = f'{conf.DUMP_DIR}/{dump_name}'

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(dump_path, arcname=os.path.basename(dump_name))
    shutil.rmtree(dump_path)  # Удаление исходной папки


def backup(serial: str, id_number: str, app: str):
    """
    Dump acc WA /data/data/com.whatsapp/*

    :param id_number:
    :param serial:
    :return: Bool Status
    """
    # Заливаем скрипт
    std_out = open(os.devnull, 'w')

    r = subprocess.run([f"adb -s {serial} push  {conf.FILES_DIR}/create_dump{'_b' if app == 'com.whatsapp.w4b' else ''} {config.PHONE_TMP_FOLDER}"],
        shell=True,
        input=None,
        stdout=std_out,
        stderr=subprocess.STDOUT
    )
    if r.returncode != 0:
        raise Exception('Fail push scripts')

    r = subprocess.run([f"adb -s {serial} shell su - root -c \"sh {config.PHONE_TMP_FOLDER}/create_dump{'_b' if app == 'com.whatsapp.w4b' else ''} {id_number}\""],  # делаем бекап
        shell=True,
        input=None,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
    if r.returncode != 0:
        raise Exception(f'Fail run script {serial}')

    r = subprocess.run([f"adb -s {serial} pull {config.PHONE_TMP_FOLDER}/{id_number} {conf.DUMP_DIR}"],  # загружаем дамп
                       shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise Exception('Fail dump WA acc')

    r = subprocess.run([f'adb -s {serial} shell su - root -c "rm -r {config.PHONE_TMP_FOLDER}/{id_number}"'],  # удаляем ненужный дамп
                       shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise Exception('Fail delete dump')

    std_out.close()
