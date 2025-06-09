from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from trident.backend.common import get_session, get_function
from trident.backend.tensorflow_backend import Layer
from trident.backend.tensorflow_ops import *
__all__ = ['l1_reg', 'l2_reg', 'orth_reg', 'get_reg', 'total_variation_norm_reg']
_session = get_session()
_epsilon = _session.epsilon

def l1_reg(model: Layer, reg_weight=1e-06):
    loss = 0.0
    for (name, param) in model.named_parameters():
        if param.trainable:
            param_ = where(is_abnormal_number(param.value()), zeros_like(param), param.value())
            if 'bias' not in name:
                loss = loss + reg_weight * reduce_sum(abs(param_))
    return loss

def l2_reg(model: Layer, reg_weight=1e-06):
    loss = 0.0
    for (name, param) in model.named_parameters():
        if param.trainable:
            param_ = where(is_abnormal_number(param.value()), zeros_like(param), param.value())
            if 'bias' not in name:
                loss = loss + reg_weight * reduce_sum(square(param_))
    return loss

def orth_reg(model: tf.Module, reg_weight=1e-06):
    loss = 0.0
    for param in model.trainable_weights:
        if param.trainable:
            if not any_abnormal_number(param) and param.trainable:
                param_flat = tf.reshape(param, (param.int_shape[0], -1))
                sym = tf.math.multiply(param_flat, tf.transpose(param_flat))
                sym -= tf.eye(param_flat.int_shape[0])
                loss = loss + reduce_sum(reg_weight * abs(sym))
    return loss

def total_variation_norm_reg(output: tf.Tensor, reg_weight=1e-06):
    diff_i = tf.math.reduce_sum(tf.math.pow(output[:, :, 1:, :] - output[:, :, :-1, :], 2))
    diff_j = tf.math.reduce_sum(tf.math.pow(output[:, 1:, :, :] - output[:, :-1, :, :], 2))
    tv_loss = diff_i + diff_j
    loss = reg_weight * tv_loss
    return loss

def get_reg(reg_name):
    if reg_name is None:
        return None
    if '_reg' not in reg_name:
        reg_name = reg_name + '_reg'
    reg_modules = ['trident.optims.tensorflow_regularizers']
    reg_fn = get_function(reg_name, reg_modules)
    return reg_fn