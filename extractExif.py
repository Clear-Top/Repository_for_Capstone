from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

# import pandas as pd
# import requests
# import sys
# import json
# import datetime

# import requests
# from urllib.parse import urlparse
# def get_labeled_exif(exif):
#     labeled = {}
#     for (key, val) in exif.items():
#         labeled[TAGS.get(key)] = val
#     return labeled
# APP_KEY = ''
# url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x=127.1086228&y=37.4012191"

# 날짜정보추출


def get_exif_time(filename):
    info = get_exif("static/uploads/"+filename)
    try:
        if info[36867] is not None:
            make_time = info[36867]
            return make_time
        else:
            return None
    except:
        return None

# 인자 : 이미지경로 , 반환값 : 모든메타정보
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds
    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(
        geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(
        geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)


# print(get_exif_time())
# print(get_coordinates(get_geotagging(get_exif("static/images/test.jpg"))))


# # 지오코딩
# address = '서울 종로구 평동 233 3106호'
# url = 'https://dapi.kakao.com/v2/local/search/address.json?&query=' + address
# result = requests.get(urlparse(url).geturl(), headers={
#                       'Authorization': 'KakaoAK 99dc47651e0b80e1160d836211f9c8d9'}).json()
# match_first = result['documents'][0]['address']
# lat = float(match_first['y'])
# lng = float(match_first['x'])
# print(lat, lng)  # 위도(lat) 경도(long)


# # 지오코딩 2
# url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x=127.1086228&y=37.4012191"
# headers = {"Authorization": "KakaoAK 99dc47651e0b80e1160d836211f9c8d9"}
# api_test = requests.get(url, headers=headers)
# url_text = json.loads(api_test.text)
# url_text
# url_text['documents'][0]['address_name']
