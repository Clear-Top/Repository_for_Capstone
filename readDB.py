import pymysql
import db


def data(curs, conn):

    # db 연결
    # conn = db.connect_db()
    # curs = conn.cursor()

    # 명령어 저장
    sql = "select carnum from class1"

    # 명령어 실행
    curs.execute(sql)
    conn.commit()
    data = curs.fetchall()

    # 데이터반환
    return data
