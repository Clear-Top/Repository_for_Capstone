import cv2
import itertools, os, time
import numpy as np
from crnn_model import get_Model
from crnn_parameter import letters
import argparse
from keras import backend as K
#K.set_learning_phase(0)
# Get CRNN model
model = get_Model(training=False)

try:
    model.load_weights("./DL/model/lpr/best2.hdf5")
    print("...Previous weight data...")
except:
    raise Exception("No weight file!")
Region = {"A": "서울 ", "B": "경기 ", "C": "인천 ", "D": "강원 ", "E": "충남 ", "F": "대전 ",
            "G": "충북 ", "H": "부산 ", "I": "울산 ", "J": "대구 ", "K": "경북 ", "L": "경남 ",
            "M": "전남 ", "N": "광주 ", "O": "전북 ", "P": "제주 "}
Hangul = {"dk": "아", "dj": "어", "dh": "오", "dn": "우", "qk": "바", "qj": "버", "qh": "보", "qn": "부",
            "ek": "다", "ej": "더", "eh": "도", "en": "두", "rk": "가", "rj": "거", "rh": "고", "rn": "구",
            "wk": "자", "wj": "저", "wh": "조", "wn": "주", "ak": "마", "aj": "머", "ah": "모", "an": "무",
            "sk": "나", "sj": "너", "sh": "노", "sn": "누", "fk": "라", "fj": "러", "fh": "로", "fn": "루",
            "tk": "사", "tj": "서", "th": "소", "tn": "수", "gj": "허", "gk": "하", "gh": "호"}

def crnn_predict(img):
    """
    Region = {"A": "서울 ", "B": "경기 ", "C": "인천 ", "D": "강원 ", "E": "충남 ", "F": "대전 ",
            "G": "충북 ", "H": "부산 ", "I": "울산 ", "J": "대구 ", "K": "경북 ", "L": "경남 ",
            "M": "전남 ", "N": "광주 ", "O": "전북 ", "P": "제주 "}
    Hangul = {"dk": "아", "dj": "어", "dh": "오", "dn": "우", "qk": "바", "qj": "버", "qh": "보", "qn": "부",
            "ek": "다", "ej": "더", "eh": "도", "en": "두", "rk": "가", "rj": "거", "rh": "고", "rn": "구",
            "wk": "자", "wj": "저", "wh": "조", "wn": "주", "ak": "마", "aj": "머", "ah": "모", "an": "무",
            "sk": "나", "sj": "너", "sh": "노", "sn": "누", "fk": "라", "fj": "러", "fh": "로", "fn": "루",
            "tk": "사", "tj": "서", "th": "소", "tn": "수", "gj": "허", "gk": "하", "gh": "호"}
    """
    def decode_label(out):
        # out : (1, 32, 42)
        out_best = list(np.argmax(out[0, 2:], axis=1))  # get max index -> len = 32
        out_best = [k for k, g in itertools.groupby(out_best)]  # remove overlap value
        outstr = ''
        for i in out_best:
            if i < len(letters):
                outstr += letters[i]
        return outstr


    def label_to_hangul(label):  # eng -> hangul
        region = label[0]
        two_num = label[1:3]
        hangul = label[3:5]
        four_num = label[5:]

        try:
            if region != 'Z':
                if '0'<=region and region<='9':
                    region = region
                else:
                    region = Region[region] 
            else:
                region = ''
        except:
            pass
        try:
            hangul = Hangul[hangul]
        except:
            pass
        return region + two_num + hangul + four_num

    """
    # Get CRNN model
    model = get_Model(training=False)

    try:
        model.load_weights("./DL/model/lpr/best2.hdf5")
        print("...Previous weight data...")
    except:
        raise Exception("No weight file!")
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_pred = img.astype(np.float32)
    img_pred = cv2.resize(img_pred, (128, 64))
    img_pred = (img_pred / 255.0) * 2.0 - 1.0
    img_pred = img_pred.T
    img_pred = np.expand_dims(img_pred, axis=-1)
    img_pred = np.expand_dims(img_pred, axis=0)
    net_out_value = model.predict(img_pred)
    pred_texts = decode_label(net_out_value)
    return label_to_hangul(pred_texts)
