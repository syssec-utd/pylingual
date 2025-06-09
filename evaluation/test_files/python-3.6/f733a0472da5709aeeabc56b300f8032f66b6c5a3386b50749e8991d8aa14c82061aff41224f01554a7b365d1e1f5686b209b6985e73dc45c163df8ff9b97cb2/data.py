import cv2 as cv
from functools import lru_cache
import glob
import numpy as np
from .symbol import Symbol

def get_alphabet() -> list[Symbol]:
    res = []
    for img_name in glob.glob('recognizer/data/*.png'):
        s = Symbol()
        img = cv.imread(img_name, cv.IMREAD_GRAYSCALE)
        (ret2, th2) = cv.threshold(img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        thresh = cv.morphologyEx(th2, cv.MORPH_CLOSE, kernel)
        (contours, _) = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        (x, y, w, h) = cv.boundingRect(contours[0])
        img_c = thresh[y:y + h, x:x + w].copy()
        mn = img_c.mean()
        fmin = img_c < mn
        fmax = img_c >= mn
        img_c[fmin] = 0
        img_c[fmax] = 255
        s.vector = img_c
        s.vector = s.vector / np.linalg.norm(s.vector)
        s.sym_mapper = img_name.split('/')[-1].replace('.png', '').replace('_', '')
        res.append(s)
    return res