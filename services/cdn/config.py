class CDNConfig:

    USER: str
    PASS: str

    URL: str
    BUCKET: str

    class Folders:
        APKS: str = 'apks'
        BACKUPS: str = 'backups'
        PHOTOS: str = 'photos'
        SCREEN_SHOTS: str = 'screens'


class SelectelConfig(CDNConfig):

    USER = "80136_ctwa"
    PASS = "N<WB0Zh?cp"

    URL = 'https://api.selcdn.ru/v1'
    BUCKET = 'SEL_80136'

    class Folder(CDNConfig.Folders): ...


class MinioConfig(CDNConfig):
    USER = "webscreen"
    PASS = "Ox4XIcOlSN77XhzLpQPiqclXm7Nch5bNWOCsE3gMx"

    URL = 'uhome-minio.k8s.caltat.net'
    BUCKET = 'ctwa'

    class Folder(CDNConfig.Folders): ...
