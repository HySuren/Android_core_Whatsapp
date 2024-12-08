import os

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .base_cdn import BaseCDN
from .config import SelectelConfig


class SelectelCDN(BaseCDN):

    CDN_CONF = SelectelConfig

    def __get_token(self) -> str:

        with requests.Session() as session:
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            response = session.get(
                'https://api.selcdn.ru/auth/v1.0',
                headers={
                    "X-Auth-User": self.CDN_CONF.USER,
                    "X-Auth-Key": self.CDN_CONF.PASS
                }
            )
        if response.status_code == 204:
            return response.headers.get('X-Auth-Token')

    def folder_file_list(self, sdn_folder_name: str):
        folder_sdn_url = f'{self.CDN_CONF.URL}/{self.CDN_CONF.BUCKET}/{sdn_folder_name}/'
        response = requests.get(
            folder_sdn_url,
            headers={
                'X-Auth-Token': self.__get_token()
            },
            stream=True)
        if response.status_code == 200:
            return [file_name.split("/")[-1] for file_name in list(response.text.split())]

    def upload_file(self, file_name: str, file_folder_path: str, sdn_folder_name: str, post_delete: bool = True) -> str:

        if file_name not in os.listdir(file_folder_path):
            raise FileExistsError(f'File {file_name} not exists!')

        with open(f'{file_folder_path}/{file_name}', 'rb') as f:
            data = f.read()

        file_sdn_url = f'{self.CDN_CONF.URL}/{self.CDN_CONF.BUCKET}/{sdn_folder_name}/{file_name}'
        response = requests.put(file_sdn_url, data=data, headers={'X-Auth-Token': self.__get_token()})
        if response.status_code == 201:
            if post_delete:
                os.remove(f'{file_folder_path}/{file_name}')
            return file_sdn_url
        else:
            raise Exception(f'ERROR upload file {file_name} in selcdn.ru\n {response.text}')

    def download_file(self, file_name: str, file_folder_path: str, sdn_folder_name: str, custom_filename: bool = False) -> None:

        response = requests.get(
            f'{self.CDN_CONF.URL}/{self.CDN_CONF.BUCKET}/{sdn_folder_name}/{file_name}',
            stream=True,
            headers={
                'X-Auth-Token': self.__get_token()
            },
            timeout=60  # Таймаут на реквест, чтобы не пендился
        )

        if response.status_code != 200:
            raise Exception(
                f'ERROR download file {file_name} from selcdn.ru\n Status code response {response.status_code}')

        if custom_filename:
            with open(file_folder_path, 'wb') as f:
                f.write(response.content)
        else:
            with open(f'{file_folder_path}/{file_name.split("/")[-1]}', 'wb') as f:
                f.write(response.content)

    def remove_file(self, file_name, sdn_folder_name):
        requests.delete(
            f'{self.CDN_CONF.URL}/{self.CDN_CONF.BUCKET}/{sdn_folder_name}/{file_name}',
            headers={
                'X-Auth-Token': self.__get_token()
            }
        )
