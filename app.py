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
UPLOAD_FOLDER = '/static/uploads/'
RESULT_FOLDER = '/result/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_EXCEL = set(['xlsx','xls'])
kor_dict   = ["가", "나", "다", "라", "마", "거", "너", "더", "러",
              "머", "버", "서", "어", "저", "고", "노", "도", "로",
              "모", "보", "소", "오", "조", "구", "누", "두", "루",
              "무", "부", "수", "우", "주", "허", "하", "호"]
num_dict   = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
app = Flask(__name__)





def allowed_excel(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXCEL


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
        if file and allowed_excel(file.filename) :
            file.save(os.path.join(os.getcwd()+'/static/excel/',file.filename))
            #엑셀업로드+db반영
            conn=db.connect_db()
            db.insert_test(file.filename,conn)
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
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            print(file.filename)
            
            full_image,plates = lpd(file)

            plate_num = []
            plate_prob = []
            print("[SYS] lpr ")
            for i,pic in enumerate(plates):
                if pic is not None:
                    try:
                        print("[",i,"]",pic.shape)
                        lp,prob = lpr(pic)
                        plate_num.append(lp[0])
                        plate_prob.append(float(prob[0][0]))
                        cv.imwrite("result/"+full_image[:-4]+"_result"+str(i)+".jpg", pic.astype(np.uint8))
                    except:
                        continue
            for i in range(len(plate_num)):
                try:
                    print("[PROB ",i,"]", plate_num[i],len(plate_num[i]))
                    if plate_num[i][-5] not in kor_dict:
                        print("wrong assumption")
                    else:
                        if (len(plate_num[i]) == 6 or len(plate_num[i]) == 7):
                            print("right length")
                        else:
                            print("wrong length")
                except:
                    print(i,"index out of range")
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=full_image,
                                   img_src=UPLOAD_FOLDER + full_image,
                                   lpd_src=RESULT_FOLDER + full_image[:-4]+"_result0.jpg")
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
