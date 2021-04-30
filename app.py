import os
from flask import Flask, render_template, request
<<<<<<< HEAD
import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
from lpd import lpd 

UPLOAD_FOLDER = '/static/uploads/'
RESULT_FOLDER = '/result/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
=======
import os.path
import cv2 as cv

UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'xlsx'])


"""
#model configuration & weight file for License Plate Detection
"""
lpdcfg = "yolov4-ANPR.cfg"
lpdweight = "yolov4-ANPR.weights"
lpdnet = cv.dnn.readNetFromDarknet(lpdcfg, lpdweight)
lpdnet.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
lpdnet.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

>>>>>>> 614e37ee8633ff5a720e71a3a1ad0f4f1654b95a

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def allowed_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
<<<<<<< HEAD
def home_page():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')
=======
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            print(file.filename);
            # call the OCR function on it
            # TODO: LPD


            # TODO: SR
            
            
            # TODO: OCR
            

            # extract the text and display it
            return render_template('upload.html')
    elif request.method == 'GET':
        return render_template('upload.html')
>>>>>>> 614e37ee8633ff5a720e71a3a1ad0f4f1654b95a

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            print(file.filename);
            # call the OCR function on it
            license_plate_detect,location_list = lpd(file)
            for i,pic in enumerate(location_list):
                cv.imwrite("result/"+license_plate_detect[:-4]+"_result"+str(i)+".jpg", pic.astype(np.uint8));
            # extract the text and display it
            print(RESULT_FOLDER + license_plate_detect[:-4]+"_result0.jpg")
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=license_plate_detect,
                                   img_src=UPLOAD_FOLDER + license_plate_detect,
                                   lpd_src=RESULT_FOLDER + license_plate_detect[:-4]+"_result0.jpg")
    elif request.method == 'GET':
        return render_template('upload.html')

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True)
=======
if __name__=='__main__':
    app.run(host='0.0.0.0')
>>>>>>> 614e37ee8633ff5a720e71a3a1ad0f4f1654b95a
