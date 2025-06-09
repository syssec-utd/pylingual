import sys
import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
import onnx_graphsurgeon as gs
from onnx2tf.utils.common_functions import get_constant_or_variable, print_node_info, inverted_operation_enable_disable, make_tf_node_info
from onnx2tf.utils.colors import Color

@print_node_info
@inverted_operation_enable_disable
def make_node(*, graph_node: gs.Node, tf_layers_dict: dict, **kwargs: dict):
    """GridSample

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    before_op_output_shape_trans_1 = tf_layers_dict.get(graph_node.inputs[0].name, {}).get('before_op_output_shape_trans', True)
    before_op_output_shape_trans_2 = tf_layers_dict.get(graph_node.inputs[1].name, {}).get('before_op_output_shape_trans', True)
    before_op_output_shape_trans = before_op_output_shape_trans_1 and before_op_output_shape_trans_2
    graph_node_input_1 = get_constant_or_variable(graph_node.inputs[0], before_op_output_shape_trans)
    graph_node_input_2 = get_constant_or_variable(graph_node.inputs[1], before_op_output_shape_trans)
    graph_node_output: gs.Variable = graph_node.outputs[0]
    shape = graph_node_output.shape
    dtype = graph_node_output.dtype
    tf_layers_dict[graph_node_output.name] = {'optype': graph_node.op, 'shape': shape, 'dtype': dtype}
    image = tf_layers_dict[graph_node_input_1.name]['tf_node'] if isinstance(graph_node_input_1, gs.Variable) else graph_node_input_1
    grid = tf_layers_dict[graph_node_input_2.name]['tf_node'] if isinstance(graph_node_input_2, gs.Variable) else graph_node_input_2
    align_corners = bool(graph_node.attrs.get('align_corners', 0))
    mode = graph_node.attrs.get('mode', 'bilinear')
    padding_mode = graph_node.attrs.get('padding_mode', 'zeros')
    if not align_corners:
        print(f'{Color.RED}ERROR:{Color.RESET} ' + f'The current implementation of GridSample supports only align_corners=1. ' + f'Pull requests are welcome. \n' + f'align_corners: 0')
        sys.exit(1)
    ENABLE_MODES = ['bilinear']
    if mode not in ENABLE_MODES:
        print(f'{Color.RED}ERROR:{Color.RESET} ' + f'The current implementation of GridSample supports only mode={ENABLE_MODES}. ' + f'Pull requests are welcome. \n' + f'mode: {mode}')
        sys.exit(1)
    ENABLE_PADDING_MODES = ['zeros']
    if padding_mode not in ENABLE_PADDING_MODES:
        print(f'{Color.RED}ERROR:{Color.RESET} ' + f'The current implementation of GridSample supports only mode={ENABLE_PADDING_MODES}. ' + f'Pull requests are welcome. \n' + f'mode: {padding_mode}')
        sys.exit(1)
    '\n    image\n        [N, H, W, C]\n    grid\n        [N, grid_H, grid_W, 2]\n    '
    Nt, H, W, C = image.shape
    grid_H = grid.shape[1]
    grid_W = grid.shape[2]
    xgrid, ygrid = tf.split(value=grid, num_or_size_splits=2, axis=-1)
    mask = tf.cast((xgrid >= 0) & (ygrid >= 0) & (xgrid < W - 1) & (ygrid < H - 1), dtype=tf.float32)
    x0 = tf.math.floor(xgrid)
    x1 = x0 + 1
    y0 = tf.math.floor(ygrid)
    y1 = y0 + 1
    wa = tf.transpose(a=(x1 - xgrid) * (y1 - ygrid), perm=[3, 0, 1, 2])
    wb = tf.transpose(a=(x1 - xgrid) * (ygrid - y0), perm=[3, 0, 1, 2])
    wc = tf.transpose(a=(xgrid - x0) * (y1 - ygrid), perm=[3, 0, 1, 2])
    wd = tf.transpose(a=(xgrid - x0) * (ygrid - y0), perm=[3, 0, 1, 2])
    x0 = tf.cast(tf.reshape(tensor=x0 * mask, shape=[Nt, grid_H, grid_W]), dtype=tf.int64)
    y0 = tf.cast(tf.reshape(tensor=y0 * mask, shape=[Nt, grid_H, grid_W]), dtype=tf.int64)
    x1 = tf.cast(tf.reshape(tensor=x1 * mask, shape=[Nt, grid_H, grid_W]), dtype=tf.int64)
    y1 = tf.cast(tf.reshape(tensor=y1 * mask, shape=[Nt, grid_H, grid_W]), dtype=tf.int64)
    ind = tf.range(limit=Nt)
    ind = tf.reshape(tensor=ind, shape=[Nt, 1])
    ind = tf.tile(input=ind, multiples=[1, grid_H])
    ind = tf.reshape(tensor=ind, shape=[Nt, grid_H, 1])
    ind = tf.tile(input=ind, multiples=[1, 1, grid_W])
    ind = tf.cast(ind, dtype=tf.int64)
    image = tf.transpose(a=image, perm=[3, 0, 1, 2])
    output_tensor = image[:, ind, y0, x0] * wa + image[:, ind, y1, x0] * wb + image[:, ind, y0, x1] * wc + image[:, ind, y1, x1] * wd
    output_tensor = tf.transpose(a=output_tensor, perm=[1, 2, 3, 0])
    mask = tf.tile(input=mask, multiples=[1, 1, 1, C])
    tf_layers_dict[graph_node_output.name]['tf_node'] = output_tensor = output_tensor * mask
    tf_layers_dict[graph_node_output.name]['tf_node_info'] = make_tf_node_info(node_info={'tf_op_type': 'GridSample', 'tf_inputs': {'image': image, 'grid': grid, 'align_corners': align_corners, 'mode': mode, 'padding_mode': padding_mode}, 'tf_outputs': {'output': tf_layers_dict[graph_node_output.name]['tf_node']}})