import os
from flask import Flask, render_template, request
import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
import db
from lpd import lpd
from lpr import lpr
import searchCar
import writeExcel
import extractExif

UPLOAD_FOLDER = '/static/uploads/'
RESULT_FOLDER = '/result/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXCEL = set(['xlsx', 'xls'])
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
    return render_template('index.html')


@app.route('/map')
def map():
    return render_template('mapPage.html')


@app.route('/xlupload', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_excel(file.filename):
            file.save(os.path.join(os.getcwd()+'/static/excel/', file.filename))
            # 엑셀업로드+db반영
            conn = db.connect_db()
            db.insert_test(file.filename, conn)
            conn.close()
            return 'success'
    elif request.method == 'GET':
        return render_template('mapPage.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # make excel pointer in advance
            excel = writeExcel.write_excel_prepare()
            writeExcel.write_excel_init(excel)

            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            # print(file.filename)

            # extract EXIF (위도,경도,시간 등등)
            info = extractExif.get_exif("static/uploads/"+file.filename)
            if info is not None:
                time = extractExif.get_exif_time(file.filename)
                lalo = extractExif.get_coordinates(get_geotagging(
                    info))
            else:
                time = None
                lalo = None

            # print(time)
            # print(lalo)

            full_image, plates = lpd(file)

            plate_num = []
            plate_prob = []
            print(file.filename)

            full_image, plates = lpd(file)

            plate_num = []
            print("[SYS] lpr ")
            for i, pic in enumerate(plates):
                if pic is not None:
                    try:
                        print("[", i, "]", pic.shape)
                        #pic = cv.resize( pic, None, fx = 3, fy = 3, interpolation = cv.INTER_CUBIC)
                        lp, prob = lpr(pic)
                        plate_num.append(lp)
                        plate_prob.append(float(prob[0][0]))
                        cv.imwrite(
                            "result/"+full_image[:-4]+"_result"+str(i)+".jpg", pic.astype(np.uint8))
                    except:
                        continue
            for i in range(len(plate_num)):
                print("[PROB ", i, "]", plate_num[i], plate_prob[i])
                carnum = plate_num[i]
                # !!!추론결과가 나올때마다 액셀에 미리저장 (일단은 로컬에 곧바로 저장 -> 추후에 save버튼눌러야 저장되게끔 구현예정)
                writeExcel.write_excel(
                    excel, plate_num[i][0], 'test', time, UPLOAD_FOLDER, file.filename, lalo)
                print("[", i, "]", pic.shape)
                pic = cv.resize(pic, None, fx=3, fy=3,
                                interpolation=cv.INTER_CUBIC)
                plate_num.append(lpr(pic))

                cv.imwrite(
                    "result/"+full_image[:-4]+"_result"+str(i)+".jpg", pic.astype(np.uint8))

            for i in plate_num:
                print(i)

            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=full_image,
                                   img_src=UPLOAD_FOLDER + full_image,
                                   lpd_src=RESULT_FOLDER + full_image[:-4]+"_result0.jpg")
    elif request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
