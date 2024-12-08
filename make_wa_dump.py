import subprocess
import uiautomator2 as u2
import sys
import os


class Phone:
    def __init__(self):
        self.d = u2.connect()
        self.serial = self.d.serial

    @staticmethod
    def copy_databases_to_sdcard():
        subprocess.run([f"adb shell su - root -c \"cp -R /data/data/com.whatsapp/databases/ /sdcard/;\""], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def download_backup(self):
        subprocess.run([f"mkdir {self.serial}"], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run([f"adb pull sdcard/databases {self.serial}/{self.get_count_dir_in_dir() + 1}"], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def download_wa(self):
        subprocess.run([f"adb pull sdcard/com.whatsapp"], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def get_count_dir_in_dir(self):
        folder_path = f"{self.serial}"
        file_list = os.listdir(folder_path)

        dir_count = 0

        for item in file_list:
            if os.path.isdir(os.path.join(folder_path, item)):
                dir_count += 1

        return dir_count

    @staticmethod
    def delete_other():
        subprocess.run([f"cp databases/msgstore.db ."], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run([f"rm -rf databases"], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @staticmethod
    def copy_proxy_db_to_sdcard():
        subprocess.run([f"adb shell su - root -c \"cp -R /data/data/org.proxydroid/databases/ /sdcard/;\""], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    @staticmethod
    def copy_wa_to_sdcard():
        subprocess.run([f"adb shell su - root -c \"cp -R /data/data/com.whatsapp/ /sdcard/;\""], shell=True, input=None, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


    def run_wa(self):
        print(f'{self.serial} connected')
        self.copy_databases_to_sdcard()
        self.download_backup()

    def run_proxy(self):
        print(f'{self.serial} connected')
        self.copy_proxy_db_to_sdcard()
        self.download_backup()

    def run_wa_copy(self):
        print(f'{self.serial} connected')
        self.copy_wa_to_sdcard()
        self.download_wa()


if __name__ == '__main__':
    phone = Phone()
    match sys.argv:
        case _, '-m':
            phone.run_wa()
            phone.delete_other()
        case _, '-p':
            phone.run_proxy()
        case _, '-w':
            phone.run_wa_copy()
        case *_, :
            phone.run_wa()
