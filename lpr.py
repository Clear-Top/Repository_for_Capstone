import argparse
from time import time

import numpy as np
import cv2
import tensorflow as tf

from model import LPRNet
from loader import resize_and_normailze


classnames = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "가", "나", "다", "라", "마", "거", "너", "더", "러",
              "머", "버", "서", "어", "저", "고", "노", "도", "로",
              "모", "보", "소", "오", "조", "구", "누", "두", "루",
              "무", "부", "수", "우", "주", "허", "하", "호"
              ]


def lpr(image):
    net = LPRNet(len(classnames) + 1)
    net.load_weights("DL/model/lpr/weights_best.pb")
    x = np.expand_dims(resize_and_normailze(image), axis=0)
    return (net.predict(x, classnames))
