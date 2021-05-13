import pymysql
import readExcel
import app


def connect_db():
    conn = pymysql.connect(host='127.0.0.1', port=3307, user='root',
                           passwd='1234', db='capstone', charset='utf8')
    print('DB 연결성공')
    return conn


# def select_all():
#     try:
#         with conn.cursor() as cursor:
#             sql = "select * from class1"
#             cursor.execute(sql)
#             rs = cursor.fetchall()
#             for row in rs:
#                 print(row)
#     finally:
#         return None


def insert_test(excel_name, conn):
    # conn은 connection ,excel_name은 엑셀파일이름
    try:
        with conn.cursor() as curs:
            i = 2
            while True:
                list = []
                for j in range(2, 9):
                    a = readExcel.read_excel(i, j, excel_name)
                    if a != 0:
                        list.append(a)
                    else:
                        i = 0
                        break
                if i == 0:
                    break
                else:
                    sql = 'insert into class1 values(%s,%s,%s,%s,%s,%s,%s)'
                    curs.execute(
                        sql, (list[0], list[1], list[2], list[3], list[4], list[5], list[6]))
                    conn.commit()
                    i = i+1
    finally:
        return None


def select_data(carnum, conn, curs):
    try:
        sql = "select IFNULL(MAX(carnum), \"No\") from class1 where carnum = \'" + \
            carnum+"\';"
        print("실행한 SQL문 : "+sql)
        curs.execute(sql)
        conn.commit()
        rs = curs.fetchall()
        # for row in rs:
        #     print(row)
    finally:
        if(rs == "No"):
            return rs
        else:
            return rs[0][0]


# db 연결
# connect_db()

# insert_test()
