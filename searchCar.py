import pymysql
import db
import readDB


def read_carnum():
    conn = db.connect_db()
    curs = conn.cursor()

    data = readDB.data(curs, conn)

    # 자동차번호만 읽어오기
    carnums = []
    for i in data:
        # 자동차번호를 리스트에 저장
        carnums.append(i[0])

    conn.close()
    # print(carnums)
    return carnums


# read_carnum()
