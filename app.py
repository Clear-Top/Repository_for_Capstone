from zerodce import lowlight
import torch
import readDB
import extractExif
import writeExcel
import searchCar
from lpr import lpr
from lpd import lpd
from korlpr import korlpr
from wpodnet import wpod_inf
import db
from pymysql import NULL
import os.path
import numpy as np
import cv2 as cv
from flask import Flask, render_template, request
import os
import json
import time
import zipfile
from crnn_predict import crnn_predict
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

UPLOAD_FOLDER = '/static/uploads/'
RESULT_FOLDER = './static/result/'
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


@app.route('/introductionList')
def introductionList():
    return render_template('introductionList.html')

@app.route('/introductionMap')
def introductionMap():
    return render_template('introductionMap.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/howtolist')
def howtolist():
    return render_template('howtolist.html')

@app.route('/servicesmodel')
def servicesmodel():
    return render_template('servicesmodel.html')

@app.route('/searchCar', methods=['GET'])
def search_carnum():
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


@app.route('/searchData', methods=['GET'])
def searchData():
    temp = ""
    temp = request.args.get('id')
    data = []
    conn = db.connect_db()
    curs = conn.cursor()
    
    data = db.select_search(temp, conn, curs)

    list=[]
    dic = {'title','lati','longt','image', 'date'}

    j=0
    for i in range (data[1]):
        list.append(dict(
            title = temp,
            date = str(data[0][j]),
            image = data[0][j+1] + data[0][j+2],
            lati = data[0][j+3],
            longt = data[0][j+4]
        ))
        j = j +5

    print(list)

    return json.dumps(list)

@app.route('/selectDate', methods=['GET'])
def selectDate():
    temp = ""
    temp = request.args.get('id')
    conn = db.connect_db()
    curs = conn.cursor()
    data = []
    data = db.select_Date(temp, conn, curs)

    return json.dumps(data)

@app.route('/clearData', methods=['GET'])
def clearData():
    conn = db.connect_db()
    curs = conn.cursor()
    db.clear_Data(conn,curs)

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
            db.clear_Data(conn,curs)  #DB초기화
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


@app.route('/',methods=['GET','POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        try :   
            nowtime=time.strftime('%y%m%d_%H%M%S')
            files = request.files.getlist("file[]")
            excel = writeExcel.write_excel_prepare()
            writeExcel.write_excel_init(excel)
            u_src=[]
            time_file = []
            lalo_file = []
            lalo_excel = []
            plate_number = []
            plate_picture = []
            zipname = []
            

            print(os.getcwd())
            for file in files :
            # check if the post request has the file part
                if file and not allowed_file(file.filename):
                    print("[SYS] NOT ALLOWED FORMAT",file.filename)
                    continue
                print("[SYS] Saving image")
                file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
                
                print("[SYS]",os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
                # extract EXIF (위도,경도,시간 등등)
                info = extractExif.get_exif("static/uploads/"+file.filename)
                if info is not None:
                    try:
                        real_time=extractExif.get_exif_time(file.filename)
                        real_lalo=extractExif.get_coordinates(extractExif.get_geotagging(info))
                        time_file.append(real_time)
                        lalo_file.append(real_lalo)
                        lalo_excel.append(real_lalo[0])
                        lalo_excel.append(real_lalo[1])
                    except:
                        real_time='None'
                        lalo_excel.append('None')
                        lalo_excel.append('None') 
                        time_file.append('None')
                        lalo_file.append('None')
                else:
                    real_time='None'
                    lalo_excel.append('None')
                    lalo_excel.append('None')
                    time_file.append('None')
                    lalo_file.append('None')
                
                print("[ZERODCE] enhancing")
                try:
                    with torch.no_grad():
                        lowlight(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
                except Exception as ll:
                    print("[ZeroDCE error]",ll)
                full_image, yolo_lp, cars = lpd(file)
                upload_source = []
                plate_num = []
                plates = []

                print("[SYS] cars")

                #Depend on Car Detection -> Wpod Net to stretch
                for i, c in enumerate(cars):
                    try:
                        img = wpod_inf(c)
                        cv.imwrite("./static/result/"+full_image.rsplit(".")[0]+"_wp"+str(i)+".jpg", img.astype(np.uint8))
                        cv.imwrite("./static/result/"+full_image.rsplit(".")[0]+"_car"+str(i)+".jpg", c.astype(np.uint8))
                        upload_source.append("/static/result/"+full_image.rsplit(".")[0]+"_wp"+str(i)+".jpg")
                        zipname.append(full_image.rsplit(".")[0]+"_wp"+str(i)+".jpg")
                        plates.append(img)
                    except Exception as e:
                        print("[ERROR]", e)
                #Depend on Yolo_lp Detection 
                if len(plates) == 0:
                    print("[Plate NOT FOUND], Using [Yolo] Instead")
                    n = 0
                    for lp in yolo_lp:
                        try:
                            cv.imwrite("./static/result/"+full_image.rsplit(".")[0]+"_yv4_"+str(n)+".jpg",lp.astype(np.uint8))
                            plates.append(lp)
                            upload_source.append("/static/result/"+full_image.rsplit(".")[0]+"_yv4_"+str(n)+".jpg")
                            zipname.append(full_image.rsplit(".")[0]+"_yv4_"+str(n)+".jpg")
                            n+=1
                        except:
                            continue
                    
                print("[SYS] lpr with correction")
                for i, pic in enumerate(plates):
                    if pic is not None:
                        try:
                            print("[", i, "]", pic.shape)
                            lp, _ = lpr(pic)
                            crnn_lp = crnn_predict(pic)
                            #print(type(lp[0]),type(crnn_lp))
                            print("[LPRNet]",lp[0])
                            print("[CRNN]",crnn_lp)
                            final_lpr = korlpr(lp[0],crnn_lp)
                            plate_num.append(final_lpr)
                            writeExcel.write_excel(excel, final_lpr, real_time, UPLOAD_FOLDER, file.filename, lalo_excel[0],lalo_excel[1],nowtime)
                        except Exception as e:
                            print("[ERROR]", e)
                plate_number.append(plate_num)
                plate_picture.append(upload_source)
                u_src.append(UPLOAD_FOLDER + full_image)
            myzip=zipfile.ZipFile('./static/result/transformed_'+nowtime+'.zip','w')
            path=os.getcwd()
            os.chdir("./static/result")
            for i in zipname:
                myzip.write(i)
            myzip.close()
            os.chdir(path)
            if(len(plate_picture)>0):
                active=1
            else:
                active=0
            return render_template('up.html',
                                    img_src=u_src,
                                    car_num=plate_number,
                                    car_time=time_file,
                                    car_lalo=lalo_file,
                                    car_source=plate_picture,
                                    nowtime=nowtime,
                                    active=active,
                                    alert=0)
        except Exception as e:
            print("[SYS]",e)
            alert=-1
            active=0
            return render_template('up.html',alert=alert,active=active)
    elif request.method == 'GET':
        active=0
        return render_template('up.html',active=active)

if __name__ == '__main__':
    app.run(debug=True)
