import os
from flask import Flask, render_template, request
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


app = Flask(__name__)
app.debug = True


def allowed_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
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


if __name__=='__main__':
    app.run(host='0.0.0.0')