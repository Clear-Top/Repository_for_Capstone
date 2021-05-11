import pymysql
import db


def data(curs, conn):

    # db 연결
    # conn = db.connect_db()
    # curs = conn.cursor()

    # 자동차번호만 추출
    sql = "select carnum from class1"

    # 명령어 실행
    curs.execute(sql)
    conn.commit()
    data = curs.fetchall()

    # 데이터반환
    return data
