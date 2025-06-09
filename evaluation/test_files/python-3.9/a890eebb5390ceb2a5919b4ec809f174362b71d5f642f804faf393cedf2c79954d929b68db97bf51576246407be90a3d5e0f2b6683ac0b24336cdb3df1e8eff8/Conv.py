import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
from tensorflow.python.keras.layers import Conv1D, Conv2D, Conv3D
import onnx_graphsurgeon as gs
from onnx2tf.utils.common_functions import get_constant_or_variable, get_weights_constant_or_variable, get_padding_as_op, print_node_info, inverted_operation_enable_disable, make_tf_node_info, dummy_tf_inference, transpose_with_flexing_deterrence
from typing import Any, Dict
from onnx2tf.utils.colors import Color
INF_INDEX_VALUE: int = 4294967296

@print_node_info
@inverted_operation_enable_disable
def make_node(*, graph_node: gs.Node, tf_layers_dict: dict, **kwargs: dict):
    """Conv

    Parameters
    ----------
    graph_node: gs.Node
        graph_surgeon Node

    tf_layers_dict: dict
        optype, shape, dtype, tensorflow graph
    """
    before_op_output_shape_trans_1 = tf_layers_dict.get(graph_node.inputs[0].name, {}).get('before_op_output_shape_trans', True)
    before_op_output_shape_trans = before_op_output_shape_trans_1
    graph_node_input = get_constant_or_variable(graph_node.inputs[0], before_op_output_shape_trans)
    kernel_shape = graph_node.attrs.get('kernel_shape', [])
    kernel_size = len(kernel_shape)
    input_weights = get_weights_constant_or_variable(const_or_var=graph_node.inputs[1], kernel_size=kernel_size)
    input_bias = None
    if len(graph_node.inputs) >= 3:
        input_bias = get_constant_or_variable(graph_node.inputs[2], before_op_output_shape_trans, is_bias=True)
    graph_node_output: gs.Variable = graph_node.outputs[0]
    output_tensor_shape = graph_node_output.shape
    dtype = graph_node_output.dtype
    input_tensor = tf_layers_dict[graph_node_input.name]['tf_node'] if isinstance(graph_node_input, gs.Variable) else graph_node_input
    input_weights = tf_layers_dict[input_weights.name]['tf_node'] if isinstance(input_weights, gs.Variable) else input_weights
    input_bias = tf_layers_dict[input_bias.name]['tf_node'] if isinstance(input_bias, gs.Variable) else input_bias
    input_tensor_shape = input_tensor.shape
    input_tensor_rank = len(input_tensor_shape)
    spatial_size = input_tensor_rank - 2
    input_weights_shape = input_weights.shape
    auto_pad = graph_node.attrs.get('auto_pad', 'NOTSET')
    dilations = graph_node.attrs.get('dilations', [1] * spatial_size)
    group = graph_node.attrs.get('group', 1)
    pads = graph_node.attrs.get('pads', [0, 0] * spatial_size)
    strides = graph_node.attrs.get('strides', [1] * spatial_size)
    disable_group_convolution: bool = kwargs['disable_group_convolution']
    tf_layers_dict[graph_node_output.name] = {'optype': graph_node.op, 'shape': output_tensor_shape, 'dtype': dtype, 'nhwc': True}
    onnx_input_shape = [dim if isinstance(dim, int) else None for dim in graph_node.inputs[0].shape] if graph_node.inputs[0].shape is not None else None
    tf_input_shape = [dim if isinstance(dim, int) else None for dim in input_tensor_shape]
    if onnx_input_shape is not None and len(onnx_input_shape) > 1 and (len(tf_input_shape) > 1) and (onnx_input_shape == tf_input_shape):
        shape_for_judging_skip = [dim if dim is not None else INF_INDEX_VALUE for dim in onnx_input_shape[1:]]
        if shape_for_judging_skip.count(shape_for_judging_skip[0]) != len(shape_for_judging_skip):
            if len(onnx_input_shape) == 3:
                input_tensor = transpose_with_flexing_deterrence(input_tensor=input_tensor, perm=[0, 2, 1], **kwargs)
            elif len(onnx_input_shape) == 4:
                input_tensor = transpose_with_flexing_deterrence(input_tensor=input_tensor, perm=[0, 2, 3, 1], **kwargs)
            elif len(onnx_input_shape) == 5:
                input_tensor = transpose_with_flexing_deterrence(input_tensor=input_tensor, perm=[0, 2, 3, 4, 1], **kwargs)
    '\n    Conv1D\n    Conv2D\n    Conv3D\n    DepthwiseConv2D\n    GroupConv1D\n    GroupConv2D\n    GroupConv3D\n    SeparableConv\n    '
    pad_mode = 'VALID'
    padded = False
    if auto_pad == 'NOTSET':
        if input_tensor_rank >= 2 and graph_node.inputs[0].shape is not None and (graph_node.inputs[0].shape[2:] == output_tensor_shape[2:]):
            pad_mode = 'SAME'
        elif pads != [0, 0] * spatial_size:
            input_tensor = get_padding_as_op(x=input_tensor, pads=pads)
            pad_mode = 'VALID'
            padded = True
        else:
            pad_mode = 'VALID'
    elif auto_pad == 'SAME_UPPER':
        pad_mode = 'SAME'
    elif auto_pad == 'VALID':
        pad_mode = 'VALID'
    elif auto_pad == 'SAME_LOWER':
        error_msg = f'' + f'{Color.RED}ERROR:{Color.RESET} ' + f'Invalid auto_pad attribute: {auto_pad}'
        print(error_msg)
        assert False, error_msg
    else:
        error_msg = f'' + f'{Color.RED}ERROR:{Color.RESET} ' + f'Invalid auto_pad attribute: {auto_pad}'
        print(error_msg)
        assert False, error_msg
    depthwise = input_tensor_rank == 4 and len(input_weights_shape) == 4 and (group != 1) and (not None in input_weights_shape) and (sum([1 if s == strides[0] else 0 for s in strides]) == len(strides))
    if depthwise and input_tensor_shape[-1] != None:
        depthwise = bool(group == input_tensor_shape[-1])
    if depthwise is True:
        depthwise_filter_shape = list(input_weights_shape[0:2]) + [-1, input_weights_shape[3] // group]
        input_weights = tf.reshape(input_weights, depthwise_filter_shape)
    input_weights = input_weights if not isinstance(input_weights, np.ndarray) else tf.convert_to_tensor(input_weights)
    input_bias = input_bias if not isinstance(input_bias, np.ndarray) else tf.convert_to_tensor(input_bias)
    tf_op_type = None
    if input_bias is not None:
        if not depthwise:
            if group == 1:
                tf_layers_dict[graph_node_output.name]['tf_node'] = tf.add(tf.nn.convolution(input=input_tensor, filters=input_weights, strides=strides, padding=pad_mode, dilations=dilations), input_bias)
                tf_op_type = tf.nn.convolution
            else:
                if kernel_size in (1, 2, 3) and (not disable_group_convolution):
                    print(f'{Color.YELLOW}WARNING:{Color.RESET} ' + f'This model contains GroupConvolution and is automatically optimized for TFLite, ' + f'but is not output because saved_model does not support GroupConvolution. ' + f'If saved_model is needed, specify --disable_group_convolution to retransform the model.')
                if kernel_size == 1 and (not disable_group_convolution):
                    tf_layers_dict[graph_node_output.name]['tf_node'] = tf.add(x=Conv1D(filters=input_weights.shape[-1], kernel_size=input_weights.shape[:1], strides=strides, padding=pad_mode.lower(), dilation_rate=dilations, groups=group, use_bias=False, kernel_initializer=tf.keras.initializers.constant(input_weights), name=graph_node.name)(input_tensor), y=input_bias)
                    tf_op_type = 'GroupedConvolution1D'
                elif kernel_size == 2 and (not disable_group_convolution):
                    tf_layers_dict[graph_node_output.name]['tf_node'] = tf.add(x=Conv2D(filters=input_weights.shape[-1], kernel_size=input_weights.shape[:2], strides=strides, padding=pad_mode.lower(), dilation_rate=dilations, groups=group, use_bias=False, kernel_initializer=tf.keras.initializers.constant(input_weights), name=graph_node.name)(input_tensor), y=input_bias)
                    tf_op_type = 'GroupedConvolution2D'
                else:
                    input_tensor_splits = tf.split(input_tensor, num_or_size_splits=group, axis=-1)
                    weight_splits = tf.split(input_weights, num_or_size_splits=group, axis=-1)
                    tf_layers_dict[graph_node_output.name]['tf_node'] = tf.add(tf.concat(values=[tf.nn.convolution(input=input_tensor_split, filters=weight_split, padding=pad_mode, strides=strides, dilations=dilations) for (input_tensor_split, weight_split) in zip(input_tensor_splits, weight_splits)], axis=-1), input_bias)
                    tf_op_type = tf.nn.convolution
        else:
            strides = [1] + strides + [1]
            tf_layers_dict[graph_node_output.name]['tf_node'] = tf.add(tf.nn.depthwise_conv2d(input=input_tensor, filter=input_weights, padding=pad_mode, strides=strides, dilations=dilations), input_bias)
            tf_op_type = tf.nn.depthwise_conv2d
    elif not depthwise:
        if group == 1:
            tf_layers_dict[graph_node_output.name]['tf_node'] = tf.nn.convolution(input=input_tensor, filters=input_weights, strides=strides, padding=pad_mode, dilations=dilations)
            tf_op_type = tf.nn.convolution
        else:
            if kernel_size in (1, 2, 3) and (not disable_group_convolution):
                print(f'{Color.YELLOW}WARNING:{Color.RESET} ' + f'This model contains GroupConvolution and is automatically optimized for TFLite, ' + f'but is not output because saved_model does not support GroupConvolution. ' + f'If saved_model is needed, specify --disable_group_convolution to retransform the model.')
            if kernel_size == 1 and (not disable_group_convolution):
                tf_layers_dict[graph_node_output.name]['tf_node'] = Conv1D(filters=input_weights.shape[-1], kernel_size=input_weights.shape[:1], strides=strides, padding=pad_mode.lower(), dilation_rate=dilations, groups=group, use_bias=False, kernel_initializer=tf.keras.initializers.constant(input_weights), name=graph_node.name)(input_tensor)
                tf_op_type = 'GroupedConvolution1D'
            elif kernel_size == 2 and (not disable_group_convolution):
                tf_layers_dict[graph_node_output.name]['tf_node'] = Conv2D(filters=input_weights.shape[-1], kernel_size=input_weights.shape[:2], strides=strides, padding=pad_mode.lower(), dilation_rate=dilations, groups=group, use_bias=False, kernel_initializer=tf.keras.initializers.constant(input_weights), name=graph_node.name)(input_tensor)
                tf_op_type = 'GroupedConvolution2D'
            else:
                input_tensor_splits = tf.split(input_tensor, num_or_size_splits=group, axis=-1)
                weight_splits = tf.split(input_weights, num_or_size_splits=group, axis=-1)
                tf_layers_dict[graph_node_output.name]['tf_node'] = tf.concat(values=[tf.nn.convolution(input=input_tensor_split, filters=weight_split, padding=pad_mode, strides=strides, dilations=dilations) for (input_tensor_split, weight_split) in zip(input_tensor_splits, weight_splits)], axis=-1)
                tf_op_type = tf.nn.convolution
    else:
        strides = [1] + strides + [1]
        tf_layers_dict[graph_node_output.name]['tf_node'] = tf.nn.depthwise_conv2d(input=input_tensor, filter=input_weights, padding=pad_mode, strides=strides, dilations=dilations)
        tf_op_type = tf.nn.depthwise_conv2d
    tf_layers_dict[graph_node_output.name]['tf_node_info'] = make_tf_node_info(node_info={'tf_op_type': tf_op_type, 'tf_inputs': {'input': input_tensor, 'weights': input_weights, 'bias': input_bias, 'strides': strides, 'dilations': dilations, 'padding': pad_mode, 'group': group}, 'tf_outputs': {'output': tf_layers_dict[graph_node_output.name]['tf_node']}})