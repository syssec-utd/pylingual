import os
import numpy as np
import onnxruntime

class Onnx_session:

    def __init__(self, model_path, **kwargs):
        self.device = 'cpu'
        self.providers = ['CPUExecutionProvider']
        print('providers:', self.providers)
        self.net = onnxruntime.InferenceSession(model_path, providers=self.providers)
        self.input_name = self.net.get_inputs()[0].name
        self.output_names = [output.name for output in self.net.get_outputs()]
        self.outs_len = len(self.output_names)

    def __call__(self, img):
        inp_dct = {self.input_name: img}
        outs = self.net.run(self.output_names, input_feed=inp_dct)
        return outs