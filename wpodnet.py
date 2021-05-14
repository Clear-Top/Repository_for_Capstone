import cv2
import numpy as np
from local_utils import detect_lp
from os.path import splitext
from keras.models import model_from_json

def wpod_inf(image):
    def load_model(path):
        try:
            path = splitext(path)[0]
            with open('%s.json' % path, 'r') as json_file:
                model_json = json_file.read()
            model = model_from_json(model_json, custom_objects={})
            model.load_weights('%s.h5' % path)
            #print("Loading model successfully...")
            return model
        except Exception as e:
            print(e)
    def preprocess_image(img,resize=False):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255
        if resize:
            img = cv2.resize(img, (224,224))
        return img

    wpod_net_path = "./DL/model/wpod/wpod-net.json"
    wpod_net = load_model(wpod_net_path)

    def get_plate(img, Dmax=608, Dmin=256):
        vehicle = preprocess_image(img)
        ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
        side = int(ratio * Dmin)
        bound_dim = min(side, Dmax)
        _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
        return LpImg, cor
    LpImg,cor = get_plate(image)
    #print("Detect %i plate(s) in"%len(LpImg))
    #print("Coordinate of plate(s) in image: \n", cor)
    img = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
    return img