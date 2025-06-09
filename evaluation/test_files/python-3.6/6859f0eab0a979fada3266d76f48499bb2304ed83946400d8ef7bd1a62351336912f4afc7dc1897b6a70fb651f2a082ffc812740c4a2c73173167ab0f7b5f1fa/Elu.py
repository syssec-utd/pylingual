import random
random.seed(0)
import numpy as np
np.random.seed(0)
import tensorflow as tf
import onnx_graphsurgeon as gs
from onnx2tf.utils.common_functions import get_constant_or_variable, print_node_info, inverted_operation_enable_disable, make_tf_node_info, get_replacement_parameter, pre_process_transpose, post_process_transpose

@print_node_info
@inverted_operation_enable_disable
@get_replacement_parameter
def make_node(*, graph_node: gs.Node, tf_layers_dict: dict, **kwargs: dict):
    """Elu

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
    graph_node_output: gs.Variable = graph_node.outputs[0]
    shape = graph_node_output.shape
    dtype = graph_node_output.dtype
    input_tensor = tf_layers_dict[graph_node_input.name]['tf_node'] if isinstance(graph_node_input, gs.Variable) else graph_node_input
    alpha = graph_node.attrs.get('alpha', 1.0)
    tf_layers_dict[graph_node_output.name] = {'optype': graph_node.op, 'shape': shape, 'dtype': dtype, 'nhwc': tf_layers_dict[graph_node_input.name]['nhwc'] if isinstance(graph_node_input, gs.Variable) and 'nhwc' in tf_layers_dict[graph_node_input.name].keys() else False}
    before_trans_shape = input_tensor.shape
    input_tensor = pre_process_transpose(value_before_transpose=input_tensor, param_target='inputs', param_name=graph_node.inputs[0].name, **kwargs)
    after_trans_shape = input_tensor.shape
    if 'nhwc' in tf_layers_dict[graph_node_output.name].keys() and tf_layers_dict[graph_node_output.name]['nhwc'] == True and (before_trans_shape != after_trans_shape):
        tf_layers_dict[graph_node_output.name].pop('nhwc')
    if alpha != 1.0:
        tf_layers_dict[graph_node_output.name]['tf_node'] = tf.cast(input_tensor < 0.0, tf.float32) * alpha * (tf.exp(input_tensor) - 1.0) + tf.cast(input_tensor >= 0.0, tf.float32) * input_tensor
    else:
        tf_layers_dict[graph_node_output.name]['tf_node'] = tf.nn.elu(features=input_tensor, name=graph_node.name)
    before_trans_shape = tf_layers_dict[graph_node_output.name]['tf_node'].shape
    tf_layers_dict[graph_node_output.name]['tf_node'] = post_process_transpose(value_before_transpose=tf_layers_dict[graph_node_output.name]['tf_node'], param_target='outputs', param_name=graph_node.outputs[0].name, **kwargs)
    after_trans_shape = tf_layers_dict[graph_node_output.name]['tf_node'].shape
    if 'nhwc' in tf_layers_dict[graph_node_output.name].keys() and tf_layers_dict[graph_node_output.name]['nhwc'] == True and (before_trans_shape != after_trans_shape):
        tf_layers_dict[graph_node_output.name].pop('nhwc')
    tf_layers_dict[graph_node_output.name]['tf_node_info'] = make_tf_node_info(node_info={'tf_op_type': tf.nn.elu, 'tf_inputs': {'features': input_tensor}, 'tf_outputs': {'output': tf_layers_dict[graph_node_output.name]['tf_node']}})