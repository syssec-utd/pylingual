"""Definition of powervr operator strategy."""
import re
from tvm import topi
from tvm.auto_scheduler import is_auto_scheduler_enabled
from .generic import *
from .. import op as _op

@conv2d_strategy.register('powervr')
def conv2d_strategy_powervr(attrs, inputs, out_type, target):
    """conv2d powervr strategy"""
    strategy = _op.OpStrategy()
    (data, kernel) = inputs
    (dilation_h, dilation_w) = attrs.get_int_tuple('dilation')
    (stride_h, stride_w) = attrs.get_int_tuple('strides')
    groups = attrs.groups
    layout = attrs.data_layout
    kernel_layout = attrs.kernel_layout
    if dilation_h < 1 or dilation_w < 1:
        raise ValueError('dilation should be positive value')
    if groups == 1:
        if layout == 'NCHW':
            if kernel_layout == 'OIHW':
                strategy.add_implementation(wrap_compute_conv2d(topi.powervr.conv2d_nchw_spatial_pack), wrap_topi_schedule(topi.powervr.schedule_conv2d_nchw_spatial_pack), name='conv2d_nchw_spatial_pack.powervr')
                (_, _, kh, kw) = get_const_tuple(kernel.shape)
                if kh == 3 and kw == 3 and (stride_h == 1) and (stride_w == 1) and (dilation_h == 1) and (dilation_w == 1):
                    strategy.add_implementation(wrap_compute_conv2d(topi.powervr.conv2d_nchw_winograd), wrap_topi_schedule(topi.powervr.schedule_conv2d_nchw_winograd), name='conv2d_nchw_winograd.powervr', plevel=5)
            elif re.match('OIHW\\d*o', kernel_layout):
                strategy.add_implementation(wrap_compute_conv2d(topi.powervr.conv2d_nchw_spatial_pack), wrap_topi_schedule(topi.powervr.schedule_conv2d_nchw_spatial_pack), name='conv2d_nchw_spatial_pack.powervr')
            else:
                raise RuntimeError('Unsupported weight layout {} for conv2d NCHW'.format(kernel_layout))
        elif layout == 'NHWC':
            assert kernel_layout == 'HWIO'
            if not is_auto_scheduler_enabled():
                strategy.add_implementation(wrap_compute_conv2d(topi.powervr.conv2d_nhwc_spatial_pack), wrap_topi_schedule(topi.powervr.schedule_conv2d_nhwc_spatial_pack), name='conv2d_nhwc_spatial_pack.powervr')
            else:
                strategy.add_implementation(wrap_compute_conv2d(topi.nn.conv2d_nhwc, need_auto_scheduler_layout=True), naive_schedule, name='conv2d_nhwc.powervr')
                is_winograd_applicable = False
                if len(kernel.shape) == 4:
                    (kernel_h, kernel_w, _, _) = get_const_tuple(kernel.shape)
                    is_winograd_applicable = 'float' in data.dtype and 'float' in kernel.dtype and (kernel_h == 3) and (kernel_w == 3) and (stride_h == 1) and (stride_w == 1) and (dilation_h == 1) and (dilation_w == 1)
                if is_winograd_applicable:
                    strategy.add_implementation(wrap_compute_conv2d(topi.nn.conv2d_winograd_nhwc, need_auto_scheduler_layout=True), naive_schedule, name='conv2d_nhwc.winograd', plevel=15)
        else:
            raise RuntimeError('Unsupported conv2d layout {} for powervr'.format(layout))
    elif is_depthwise_conv2d(data.shape, layout, kernel.shape, kernel_layout, groups):
        if layout == 'NCHW':
            assert kernel_layout == 'OIHW'
            strategy.add_implementation(wrap_compute_conv2d(topi.powervr.depthwise_conv2d_nchw), wrap_topi_schedule(topi.powervr.schedule_depthwise_conv2d_nchw), name='depthwise_conv2d_nchw.powervr')
        elif layout == 'NHWC':
            assert kernel_layout == 'HWOI'
            if not is_auto_scheduler_enabled():
                raise RuntimeError('depthwise_conv2d NHWC layout is not enabled for powervr without auto_scheduler.')
            strategy.add_implementation(wrap_compute_conv2d(topi.nn.depthwise_conv2d_nhwc), naive_schedule, name='depthwise_conv2d_nhwc.powervr')
        else:
            raise RuntimeError('Unsupported depthwise_conv2d layout {} for powervr'.format(layout))
    else:
        raise RuntimeError('group_conv2d is not supported for powervr')
    return strategy

@conv2d_winograd_without_weight_transfrom_strategy.register('powervr')
def conv2d_winograd_without_weight_transfrom_strategy_powervr(attrs, inputs, out_type, target):
    """conv2d_winograd_without_weight_transfrom powervr strategy"""
    dilation = attrs.get_int_tuple('dilation')
    groups = attrs.get_int('groups')
    layout = attrs.data_layout
    strides = attrs.get_int_tuple('strides')
    kernel = inputs[1]
    assert dilation == (1, 1), 'Do not support dilate now'
    assert strides == (1, 1), 'Do not support strides now'
    assert groups == 1, 'Do not supoort arbitrary group number'
    strategy = _op.OpStrategy()
    if layout == 'NCHW':
        assert len(kernel.shape) == 5, 'Kernel must be packed into 5-dim'
        strategy.add_implementation(wrap_compute_conv2d(topi.powervr.conv2d_nchw_winograd), wrap_topi_schedule(topi.powervr.schedule_conv2d_nchw_winograd), name='conv2d_nchw_winograd.powervr')
    elif layout == 'NHWC':
        if not is_auto_scheduler_enabled():
            raise RuntimeError('Winograd conv2d NHWC is not enabled for powervr without auto_scheduler.')
        strategy.add_implementation(wrap_compute_conv2d(topi.nn.conv2d_winograd_nhwc_without_weight_transform, need_auto_scheduler_layout=True), naive_schedule, name='conv2d_nhwc_winograd_without_weight_transform', plevel=15)
    else:
        raise RuntimeError('Unsupported conv2d_winograd_without_weight_transfrom layout {}'.format(layout))
    return strategy

@dense_strategy.register('powervr')
def dense_strategy_powervr(attrs, inputs, out_type, target):
    """dense powervr strategy"""
    strategy = _op.OpStrategy()
    if not is_auto_scheduler_enabled():
        strategy.add_implementation(wrap_compute_dense(topi.powervr.dense), wrap_topi_schedule(topi.powervr.schedule_dense), name='dense.powervr')
    else:
        strategy.add_implementation(wrap_compute_dense(topi.nn.dense, need_auto_scheduler_layout=True), naive_schedule, name='dense.powervr')
    return strategy