from sklearn.metrics import mean_absolute_error
import cv2
import numpy as np
from ...data.image import read_torchImage
from ...utils.util_warp import face_align
from ...utils.util_attribute import get_pred
from ...data.constant import LMARK_REF_ARC
from ..model_common import load_tensorRT, load_onnx, load_openvino, load_torch
gender_dict = {0: 'F', 1: 'M'}

class Arcface_GenderAge_cmt:

    def __init__(self, model_type, model_path, out_size=112, **kwargs):
        self.model_path = model_path
        self.out_size = out_size
        self.model_type = model_type
        if self.model_type in ['pt', 'pth']:
            self.net = load_torch.TorchModel('arcface_cmt', self.model_path, num_features=kwargs.get('num_features'), network=kwargs.get('network'))
        elif self.model_type == 'onnx':
            self.net = load_onnx.Onnx_session(self.model_path, input_mean=0.0, input_std=1.0, onnx_device=kwargs.get('onnx_device', 'cuda'))
        elif self.model_type == 'trt':
            self.net = load_tensorRT.TrtModel(self.model_path)
            self.shape = self.net.engine.get_binding_shape(0)
        elif self.model_type == 'openvino':
            self.net = load_openvino.Openvino(self.model_path, device=kwargs.get('device', 'CPU'))

    def get(self, img, face, to_bgr):
        if not 'aimg' in face.keys():
            aimg = face_align(img, LMARK_REF_ARC, face.land5, self.out_size)
            face.aimg = aimg
        else:
            aimg = face.aimg
        if self.model_type == 'onnx':
            aimg = (aimg / 255.0 - 0.5) / 0.5
        gender_outs, age_outs = self.net(aimg)
        pred_g, pred_a = get_pred(gender_outs, age_outs)
        face.gender = gender_dict[pred_g]
        face.age = pred_a
        return (face.gender, face.age)