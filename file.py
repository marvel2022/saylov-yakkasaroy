import os

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_PATH=os.path.join(BASE_DIR, f'images/stations/{574}/')
IMAGE_LIST=[]
for base, dirs, files in os.walk(IMAGE_PATH):
    for file in files:
        station_photo_path= IMAGE_PATH+"{}".format(file)
        station_photo = open(station_photo_path, 'rb')
        IMAGE_LIST.append(station_photo)
print(IMAGE_LIST)
