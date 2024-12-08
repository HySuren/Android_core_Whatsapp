import os
import shutil
import subprocess
import tarfile

import config
from services.backup import conf


def restore_dump(serial, sdn_uniq: str, app: str, cdn=config.CDN):
    cdn.download_file(sdn_uniq, conf.FILES_DIR, 'yandex/backups')
    untardir(sdn_uniq)
    restore_dump_adb(serial, sdn_uniq, app)


def untardir(tar_name: str):

    """Распаковывает tar файл в files/dump_scripts
    Принимает название tar файла в files/dump_scripts/dumps_zip/
    УДАЛЯЕТ TAR файл!"""

    if tar_name not in os.listdir(f'{conf.FILES_DIR}'):
        raise FileExistsError(f'File {tar_name} not exists!')


    with tarfile.open(f'{conf.FILES_DIR}/{tar_name}') as tar:
        tar.extractall(f'{conf.DUMP_DIR}/')
    os.remove(f'{conf.FILES_DIR}/{tar_name}')


def restore_dump_adb(serial, id_number: str, app: str):

        """ Restore dumpWA Reinstalling the dump to a NEW version of WA.apk  """

        std_out = open(os.devnull, 'w')

        if id_number not in os.listdir(path=f"{conf.FILES_DIR}/dumps/"):
            raise NameError(f'file: {id_number} not found')

        # Заливаем скрипт
        r = subprocess.run([f"adb -s {serial} push  {conf.FILES_DIR}/restore_dump{'_b' if app == 'com.whatsapp.w4b' else ''} {config.PHONE_TMP_FOLDER}"],
            shell=True,
            input=None,
            stdout=std_out,
            stderr=subprocess.STDOUT
        )
        if r.returncode != 0:
            raise Exception('Fail push scripts')

        # заливаем дамп
        r = subprocess.run([f'adb -s {serial} push {conf.DUMP_DIR}/{id_number}/ {config.PHONE_TMP_FOLDER}'],
            shell=True,
            input=None,
            stdout=std_out,
            stderr=subprocess.STDOUT
        )
        if r.returncode != 0:
            raise Exception('Fail push dump')

        # restore dump
        r = subprocess.run([f"adb -s {serial} shell su - root -c \"sh {config.PHONE_TMP_FOLDER}/restore_dump{'_b' if app == 'com.whatsapp.w4b' else ''} {id_number}\""], shell=True, input=None, stdout=std_out, )
        # удаляем ненужный дамп с телефона
        r = subprocess.run([f'adb -s {serial} shell su - root -c "rm -r {config.PHONE_TMP_FOLDER}/{id_number}"'], shell=True, input=None, stdout=std_out, stderr=subprocess.STDOUT)
        if r.returncode != 0:
            raise Exception(f'Fail delete dump({id_number}) in device')

        # удаляем ненужный дамп
        shutil.rmtree(f'{conf.FILES_DIR}/dumps/{id_number}')

        std_out.close()
