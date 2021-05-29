import pymysql
import readExcel
import app


def connect_db():
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                           passwd='root', db='capstone', charset='utf8')
    # print('DB 연결성공')
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
                for j in range(2, 8):
                    a = readExcel.read_excel(i, j, excel_name)
                    if a != 0:
                        list.append(a)
                    else:
                        i = 0
                        break
                if i == 0:
                    break
                else:
                    sql = 'insert into class1 values(%s,%s,%s,%s,%s,%s)'
                    curs.execute(
                        sql, (list[0], list[1], list[2], list[3], list[4], list[5]))
                    conn.commit()
                    i = i+1
    finally:
        return None


def select_data(carnum, conn, curs):
    try:
        sql = "select IFNULL(MAX(carnum), \"No\") from class1 where carnum = \'" + \
            str(carnum)+"\';"
        curs.execute(sql)
        conn.commit()
        global rs
        rs = curs.fetchall()
        # for row in rs:
        #     print(row)
    finally:
        return rs


def select_ALLdata(conn, curs):
    try:
        sql = "select distinct carnum from class1 order by carnum asc;"
        curs.execute(sql)
        conn.commit()
        global rs
        rs = curs.fetchall()

        listData = []
        for i in rs:
            listData.append(i[0])
            # print(i[0])
    finally:
        # print("{"+sql + "}   조회완료")
        return listData


def select_search(carnum, conn, curs):
    try:
        sql = "select date, image_path, image_name, lati, longt from class1 where carnum = \'" + \
            str(carnum)+"\' order by date asc;"
        curs.execute(sql)
        conn.commit()
        global rs
        rs = curs.fetchall()

        listData = []
        result = []
        count = 0

        for i in rs:
            j=0
            while True:
                if j == 5:
                    break
                listData.append(i[j])
                # print(i[j])
                j = j+1
                count = count + 1
                    
    finally:
        count = int(count/5)
        result.append(listData)
        result.append(count)
        return result

def select_Date(carnum, conn, curs):
    try:
        sql = "select carnum,date from class1 where carnum = '" + str(carnum) + "' order by date asc;"
        curs.execute(sql)
        conn.commit()
        global rs
        rs = curs.fetchall()

        listData = []
        # dic = {'carnum','date'} 딕셔너리 속성 값

        for i in rs:
            listData.append(dict(
            title=i[0],
            date=str(i[1])
            ))
    finally:
        # print(listData)
        return listData

def clear_Data(conn, curs):
    try:
        sql = "delete from class1;"
        curs.execute(sql)
        conn.commit()
    finally:
        return None

# 날짜 분리구문(년월일/시간)
# select carnum, date_format(date,'%Y-%m-%d'),date_format(date,'%h:%i:%s') from class1 where carnum = '12가3456' order by date asc ;

