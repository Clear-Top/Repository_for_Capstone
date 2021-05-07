import os
from flask import Flask, render_template, request
from skew_plate import rotate
import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
from lpd import lpd 
from lpr import lpr
UPLOAD_FOLDER = '/static/uploads/'
RESULT_FOLDER = '/result/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def allowed_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
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

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            print(file.filename);
            
            full_image,plates = lpd(file)

            plate_num = []
            print("[SYS] lpr ")
            for i,pic in enumerate(plates):
                if pic is not None:
                    try:
                        print(i,"     ",pic.shape)
                        pic = cv.resize( pic, None, fx = 3, fy = 3, interpolation = cv.INTER_CUBIC)
                        plate_num.append(lpr(pic))

                        cv.imwrite("result/"+full_image[:-4]+"_result"+str(i)+".jpg", pic.astype(np.uint8));
                    except:
                        continue
            for i in plate_num:
                print(i)
            print(RESULT_FOLDER + full_image[:-4]+"_result0.jpg")
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=full_image,
                                   img_src=UPLOAD_FOLDER + full_image,
                                   lpd_src=RESULT_FOLDER + full_image[:-4]+"_result0.jpg")
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
