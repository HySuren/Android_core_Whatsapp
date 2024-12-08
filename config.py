import logging
import os
from dotenv import load_dotenv

from services.cdn import SelectelCDN


def prepare_logging():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s: [%(levelname)s] %(message)s', datefmt='%d %b %H:%M:%S')
    logging.addLevelName(logging.ERROR, f"{logging.getLevelName(logging.ERROR)}")
    logging.addLevelName(logging.WARNING, f"{logging.getLevelName(logging.WARNING)}")


CDN = SelectelCDN()

PHONE_TMP_FOLDER = '/data/local/tmp'

WEB_API_DOMAIN = 'http://localhost:21465'
ENABLE_WEB_BACKUP = False
DEVICE_PAIRS = {'RZ8RB1MHR9J': 'HZQL1838HAKB1302949', 'RZ8RB1MHD4X': 'HZQL1838HAKA2901891', 'RF8RA1AATWY': 'HZQL1838HAKA3000391', 'RZ8RB1F2DTZ': 'HZQL1838HAKB0400313', 'RZ8RB0P38PT': 'HZQL1838HAKA3002450', 'RZ8RB0P38GH': 'HZQL1838HAKA3001185', 'RF8RA0TRXWK': 'HZQL1838HAKB1302631', 'RF8T11BW5MA': 'HZQL1838HAKA3002345', 'RF8RB0CXHRN': 'HZQL1838HAKA2901260', 'RF8RB1B15JX': 'HZQL1838HAKB1303006', 'RF8RA0T3WZN': 'HZQL1838HAKA3000177', 'RF8T11BW3QK': 'FS0CXM101513', 'RZ8RB1MHYBZ': '320106648726', 'RZ8RB1F2HBV': 'FS14EM102262', 'RZ8RB1K37PH': '320207317750', 'RF8T11BX1BL': '320207315315', 'RF8RB1AZDVZ': '320106648770'}
DEVICE_125 = ['RF8R806APML', 'RF8R80ADR3A', 'R58R82YG62X']
CODE_ACTIVATORS_W_CALLS = ['drop_sms']
DUPLICATE_PARAMETERS = ['id', 'reg_aggregators']

# Подгрузка переменных окружения из файла .env
load_dotenv('.env')

# dev/prod
DB_MODE = os.getenv('DB_MODE')


class DatabaseConfig:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = int(os.getenv('DB_PORT'))

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
