import pymysql
import readExcel

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
            i=2
            while True:
                list = []
                for j in range(2,9):
                    a = readExcel.read_excel(i,j)
                    if a != 0:
                        list.append(a)
                    else:
                        i=0
                        break;
                if i == 0:
                        break;
                else:
                    sql = 'insert into class1 values(%s,%s,%s,%s,%s,%s,%s)'
                    curs.execute(sql, (list[0],list[1],list[2],list[3],list[4], list[5],list[6]))
                    conn.commit()
                    i = i+1
    finally:
        conn.close()

insert_test()