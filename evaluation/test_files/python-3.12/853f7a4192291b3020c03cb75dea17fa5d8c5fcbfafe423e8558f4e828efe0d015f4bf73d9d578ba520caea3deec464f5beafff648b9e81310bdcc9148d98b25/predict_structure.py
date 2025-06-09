import os
import sys
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '../..')))
os.environ['FLAGS_allocator_strategy'] = 'auto_growth'
import cv2
import numpy as np
import time
import json
from ydocr.utility import get_model_data, get_table_character_dict, get_model_data_from_path
from preprocess import preprocess_op
from postprocess import TableLabelDecode
import onnxruntime as ort
character_dict = get_table_character_dict()
table_model_file = 'table_model_ch.onnx'

def build_pre_process_list(args):
    resize_op = {'ResizeTableImage': {'max_len': args.table_max_len}}
    pad_op = {'PaddingTableImage': {'size': [args.table_max_len, args.table_max_len]}}
    normalize_op = {'NormalizeImage': {'std': [0.229, 0.224, 0.225] if args.table_algorithm not in ['TableMaster'] else [0.5, 0.5, 0.5], 'mean': [0.485, 0.456, 0.406] if args.table_algorithm not in ['TableMaster'] else [0.5, 0.5, 0.5], 'scale': '1./255.', 'order': 'hwc'}}
    to_chw_op = {'ToCHWImage': None}
    keep_keys_op = {'KeepKeys': {'keep_keys': ['image', 'shape']}}
    if args.table_algorithm not in ['TableMaster']:
        pre_process_list = [resize_op, normalize_op, pad_op, to_chw_op, keep_keys_op]
    else:
        pre_process_list = [resize_op, pad_op, normalize_op, to_chw_op, keep_keys_op]
    return pre_process_list

def create_operators(op_param_list, global_config=None):
    """
    create operators based on the config

    Args:
        params(list): a dict list, used to create some operators
    """
    assert isinstance(op_param_list, list), 'operator config should be a list'
    ops = []
    for operator in op_param_list:
        assert isinstance(operator, dict) and len(operator) == 1, 'yaml format error'
        op_name = list(operator)[0]
        param = {} if operator[op_name] is None else operator[op_name]
        if global_config is not None:
            param.update(global_config)
        op = eval(op_name)(**param)
        ops.append(op)
    return ops

def transform(data, ops=None):
    """ transform """
    if ops is None:
        ops = []
    for op in ops:
        data = op(data)
        if data is None:
            return None
    return data

class TableStructurer(object):

    def __init__(self, ort_providers=None, table_model_path=None):
        if ort_providers is None:
            ort_providers = ['CPUExecutionProvider']
        self.preprocess_op = preprocess_op
        self.postprocess_op = TableLabelDecode(character_dict_path=character_dict, merge_no_span_structure=True)
        model_data = get_model_data(table_model_file) if table_model_path is None else get_model_data_from_path(table_model_path)
        so = ort.SessionOptions()
        so.log_severity_level = 3
        sess = ort.InferenceSession(model_data, so, providers=ort_providers)
        self.output_tensors = None
        self.predictor, self.input_tensor = (sess, sess.get_inputs()[0])

    def __call__(self, img):
        starttime = time.time()
        data = {'image': img}
        data = transform(data, self.preprocess_op)
        img = data[0]
        if img is None:
            return (None, 0)
        img = np.expand_dims(img, axis=0)
        img = img.copy()
        input_dict = {}
        input_dict[self.input_tensor.name] = img
        outputs = self.predictor.run(self.output_tensors, input_dict)
        preds = {}
        preds['structure_probs'] = outputs[1]
        preds['loc_preds'] = outputs[0]
        shape_list = np.expand_dims(data[-1], axis=0)
        post_result = self.postprocess_op(preds, [shape_list])
        structure_str_list = post_result['structure_batch_list'][0]
        bbox_list = post_result['bbox_batch_list'][0]
        structure_str_list = structure_str_list[0]
        structure_str_list = ['<html>', '<body>', '<table>'] + structure_str_list + ['</table>', '</body>', '</html>']
        elapse = time.time() - starttime
        return ((structure_str_list, bbox_list), elapse)

def draw_boxes(image, boxes, scores=None, drop_score=0.5):
    if scores is None:
        scores = [1] * len(boxes)
    for box, score in zip(boxes, scores):
        if score < drop_score:
            continue
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 0), 2)
    return image

def main():
    table_structurer = TableStructurer()
    image_file = 'img_file/table_ch_result3.jpg'
    img = cv2.imread(image_file)
    structure_res, elapse = table_structurer(img)
    print(structure_res)
    structure_str_list, bbox_list = structure_res
    img = draw_boxes(img, bbox_list)
    cv2.imwrite('table_structure.png', img)
if __name__ == '__main__':
    main()