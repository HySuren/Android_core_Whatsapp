import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(dir_path)[0].split("/common")[0])
print(sys.path)

from services.cdn import SelectelCDN


"""
Скрипт по загрузке прилы ватсапа на CDN из папки /apk
Бери во внимание, что при загрузке должна находиться одна прила, если будет несколько 
то будет рандом на какую загрузит
"""

file_name = [item for item in os.listdir('../apk') if 'wa' in item][0]
print('К загрузке:', file_name)

resp = SelectelCDN().upload_file(file_name, '../apk', 'yandex/apk', False)
print(resp)
