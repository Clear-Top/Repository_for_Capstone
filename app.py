import readDB
import extractExif
import writeExcel
import searchCar
from lpr import lpr
from lpd import lpd
from wpodnet import wpod_inf
import db
from pymysql import NULL
import os.path
import numpy as np
import sys
import argparse
import cv2 as cv
from flask import Flask, render_template, request
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


UPLOAD_FOLDER = '/static/uploads/'
RESULT_FOLDER = '/result/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXCEL = set(['xlsx', 'xls'])
kor_dict = ["가", "나", "다", "라", "마", "거", "너", "더", "러",
            "머", "버", "서", "어", "저", "고", "노", "도", "로",
            "모", "보", "소", "오", "조", "구", "누", "두", "루",
            "무", "부", "수", "우", "주", "허", "하", "호"]
num_dict = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
app = Flask(__name__)


def allowed_excel(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXCEL


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('up.html')


@app.route('/searchCar', methods=['GET'])
def search_carnum():
<<<<<<< HEAD
    if request.method == 'GET':
        toggle = 0
        temp = ""
        temp = request.args.get('search')
        print("검색한 번호 : " + temp)
        conn = db.connect_db()
        curs = conn.cursor()
        data = db.select_data(temp, conn, curs)

        print(data)

        conn.close()
        if(data == "No"):
            # print('검출실패!')
            toggle = 0
            return render_template('mapPage.html', carnum="없는 데이터입니다.", askInsert=toggle)
        else:
            # print('검출성공!')
            toggle = 1
            return render_template('mapPage.html', carnum=data, askInsert=toggle)

        # print(data)
    """else:
        print("새로고침?")
        return render_template('mapPage.html')"""
=======
    # print('submit해서 server옴')
    toggle = 0
    temp = ""
    data = ""
    temp = request.args.get('id')
    # temp = request.form.get('search', False)
    print("검색한 번호 : " + str(temp))
    conn = db.connect_db()
    curs = conn.cursor()
    if(temp == ""):
        data = db.select_ALLdata(conn, curs)
    else:
        tp = db.select_data(temp, conn, curs)
        data = tp[0]

    print(data)
    conn.close()
    if data[0] == "No":
        toggle = 0
    else:
        toggle = 1
    # print(toggle)
    json_object = {
        "carnum": data,
        "toggle": toggle
    }
    json_string = json.dumps(json_object)
    return json_string
>>>>>>> febf1d8f5fa041f6d8a9b9d6c38c48e5e7f90c3c


@app.route('/xlupload', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('mapPage.html', msg='[제출실패]')
        file = request.files['file']
        if file.filename == '':
            return render_template('mapPage.html', msg='[제출실패]')
        if file and allowed_excel(file.filename):
            file.save(os.path.join(
                os.getcwd()+'/static/excel/', file.filename))
            # 엑셀업로드+db반영
            conn = db.connect_db()  # DB연결
            curs = conn.cursor()    # cursor생성

            db.insert_test(file.filename, conn)  # test삽입

            data = readDB.data(curs, conn)
            conn.close()

            return render_template('mapPage.html', msg='[제출성공]', carnum=data)
    elif request.method == 'GET':
        return render_template('mapPage.html')
        
def search_carnum():
    if request.method == 'GET':
        toggle = 0
        temp = ""
        temp = request.args.get('search')
        print("검색한 번호 : " + temp)
        conn = db.connect_db()
        curs = conn.cursor()
        data = db.select_data(temp, conn, curs)

        print(data)

        conn.close()
        if(data == "No"):
            # print('검출실패!')
            toggle = 0
            return render_template('mapPage.html', carnum="없는 데이터입니다.", askInsert=toggle)
        else:
            # print('검출성공!')
            toggle = 1
            return render_template('mapPage.html', carnum=data, askInsert=toggle)

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('up.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('up.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # make excel pointer in advance
            excel = writeExcel.write_excel_prepare()
            writeExcel.write_excel_init(excel)

            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            print(file.filename)

            # extract EXIF (위도,경도,시간 등등)
            info = extractExif.get_exif("static/uploads/"+file.filename)
            if info is not None:
                time = extractExif.get_exif_time(file.filename)
                lalo = extractExif.get_coordinates(extractExif.get_geotagging(info))
            else:
                time = None
                lalo = None

            # print(time)
            # print(lalo)

            full_image, yolo_lp, cars = lpd(file)

            plate_num = []
            plate_prob = []
            plates = []
            # print(file.filename)
            print("[SYS] cars")
            for i, c in enumerate(cars):
                try:
                    img = wpod_inf(c)
                    cv.imwrite("result/"+full_image[:-4]+"_wp"+str(i)+".jpg", img.astype(np.uint8))
                    cv.imwrite("result/"+full_image[:-4]+"_car"+str(i)+".jpg", c.astype(np.uint8))
                    plates.append(img)
                except Exception as e:
                    try:
                        n = 0
                        for i in yolo_lp:
                            cv.imwrite("result/"+full_image[:-4]+"yv4"+str(n)+".jpg",i.astype(np.uint8))
                            n+=1
                    except Exception as ef:
                        print("[ERROR]",e,ef)
            if len(plates) == 0:
                print("[NOT FOUND]")
            print("[SYS] lpr ")
            for i, pic in enumerate(plates):
                if pic is not None:
                    try:
                        print("[", i, "]", pic.shape)
                        lp, prob = lpr(pic)
                        plate_num.append(lp[0])
                        plate_prob.append(float(prob[0][0]))
                        #cv.imwrite("result/"+full_image[:-4]+"_lp"+str(i)+".jpg", pic.astype(np.uint8))
                    except Exception as e:
                        print("[ERROR]", e)

            for i in range(len(plate_num)):
                try:
                    print("[PROB ", i, "]", plate_num[i], len(plate_num[i]))
                    if plate_num[i][-5] not in kor_dict:
                        print("wrong assumption")
                        #TODO: Implement alternative algorithm for handling
                    else:
                        if (len(plate_num[i]) == 6 or len(plate_num[i]) == 7):
                            print("right length")
                            writeExcel.write_excel(
                                excel, plate_num[i], 'test', time, UPLOAD_FOLDER, file.filename, lalo)
                        else:
                            #TODO: Implement alternative algorithm
                            print("wrong length")
                except Exception as e:
                    print("[ERROR]", e)
            return render_template('up.html',
                                   msg='Successfully processed',
                                   extracted_text=full_image,
<<<<<<< HEAD
                                   img_src=UPLOAD_FOLDER + full_image[:-16]+".jpg",
                                   lpd_src=RESULT_FOLDER + full_image[:-4]+"_wp0.jpg",
                                   car_num=plate_num[i],
                                   car_time=time,
                                   car_lalo=lalo,
                                   car_filename=file.filename)
=======
                                   img_src=UPLOAD_FOLDER + full_image,
                                   lpd_src="result/"+full_image[:-4]+"_wp0.jpg")
>>>>>>> febf1d8f5fa041f6d8a9b9d6c38c48e5e7f90c3c
    elif request.method == 'GET':
        return render_template('up.html')


if __name__ == '__main__':
    app.run(debug=True)
