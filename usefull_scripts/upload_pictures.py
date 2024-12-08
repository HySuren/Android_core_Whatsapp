import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.split(dir_path)[0].split("/common")[0])
print(sys.path)

from services.cdn import SelectelCDN

"""
Скрипт по загрузке картинок из репы /services/photos/group
На CDN заливается с неймами этих картинок, поэтому следи за названием файлов, 
чтобы было все четко
"""


# Разрешенные расширения картинок
GOOD_EXTENSIONS = ('png', 'jpg', 'jpeg', 'webp')

file_names = [item for item in os.listdir('../services/photos/group') if any(item.endswith(ext) for ext in GOOD_EXTENSIONS)]
print('Картинки к заливке:', file_names)

for file_name in file_names:
    resp = SelectelCDN().upload_file(file_name, '../services/photos/group', 'skillbox_womans/group', False)
    print(resp)
