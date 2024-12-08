import os

from minio import Minio

from .base_cdn import BaseCDN
from .config import MinioConfig


class MinioCDN(BaseCDN):

    CDN_CONF = MinioConfig

    def __init__(self):
        self._client = Minio(
            endpoint=self.CDN_CONF.URL,
            access_key=self.CDN_CONF.USER,
            secret_key=self.CDN_CONF.PASS,
        )

    def folder_file_list(self, sdn_folder_name: str) -> list[str]:
        files = self._client.list_objects(self.CDN_CONF.BUCKET, f'{sdn_folder_name}/')
        return [file.object_name.split("/")[-1] for file in files]

    def upload_file(self, file_name: str, file_folder_path: str, sdn_folder_name: str) -> str:
        if file_name not in os.listdir(file_folder_path):
            raise FileExistsError(f'File {file_name} not exists!')

        response = self._client.fput_object(
            bucket_name=self.CDN_CONF.BUCKET,
            object_name=f'{sdn_folder_name}/{file_name}',
            file_path=f'{file_folder_path}/{file_name}',
        )

        os.remove(f'{file_folder_path}/{file_name}')
        return response._location

    def download_file(self, file_name: str, file_folder_path: str, sdn_folder_name: str) -> None:
        response = self._client.get_object(self.CDN_CONF.BUCKET, f'{sdn_folder_name}/{file_name}')
        with open(f'{file_folder_path}/{file_name.split("/")[-1]}', 'wb') as f:
            f.write(response.data)

    def remove_file(self, file_name, sdn_folder_name) -> None:
        self._client.remove_object(self.CDN_CONF.BUCKET, f'{sdn_folder_name}/{file_name}')


