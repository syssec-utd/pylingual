from __future__ import absolute_import, division, print_function
from easydict import EasyDict as edict
__C = edict()
cfg = __C
'\nModel options\n'
__C.MODEL = edict()
__C.MODEL.GAUSSIAN_KSIZE = 15
__C.MODEL.GAUSSIAN_SIGMA = 0.5
__C.MODEL.DES_THRSH = 1.0
__C.MODEL.COO_THRSH = 5.0
__C.MODEL.KSIZE = 3
__C.MODEL.padding = 1
__C.MODEL.dilation = 1
__C.MODEL.scale_list = [3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0]
__C.MODEL.PIXELS = 16
__C.MODEL.RADIUS = 200
__C.MODEL.HEIGHT = 480
__C.MODEL.WIDTH = 640
__C.MODEL.FLOWC = 20
__C.MODEL.THRESHOLDPOINT = 102
'\nTraining options\n'
__C.TRAIN = edict()
__C.TRAIN.score_com_strength = 100.0
__C.TRAIN.scale_com_strength = 100.0
__C.TRAIN.NMS_THRESH = 0.0
__C.TRAIN.NMS_KSIZE = 5
__C.TRAIN.TOPK = 512
'\nThreshold options\n'
__C.Threshold = edict()
__C.Threshold.MANG = 2
__C.Threshold.ROT = 5
'\nInfer options\n'
__C.INFER = edict()
__C.INFER.ALLINFER = False