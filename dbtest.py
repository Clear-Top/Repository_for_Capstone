import pymysql
import extractExif

def select_all():
    conn = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', passwd = 'root', db = 'capstone', charset = 'utf8')
    try:
        with conn.cursor() as cursor:
            sql = "select * from class1"
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                print(row)
    finally:
        conn.close()

def insert_test():
    conn = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', passwd = 'root', db = 'capstone', charset = 'utf8')

    try:
        with conn.cursor() as curs:
            sql = 'insert into class1 values(%s,%s,%s,%s,%s,%s,%s)'
            curs.execute(sql, ('11하2232','서울시','2021-05-07','c:www',la, lo,'사진'))
        conn.commit()
    finally:
        conn.close()

exif = extractExif.get_exif('test.jpg')
geotags = extractExif.get_geotagging(exif)

la,lo = extractExif.get_coordinates(geotags)

insert_test()
select_all()

