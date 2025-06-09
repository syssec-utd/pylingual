"""Conv3D alter op and legalize functions for cuda backend"""
import logging
import tvm
from tvm import te
from tvm import relay
from tvm import autotvm
from .. import nn
from ..utils import get_const_tuple
from .conv3d_winograd import _infer_tile_size
logger = logging.getLogger('topi')

@nn.conv3d_alter_layout.register(['cuda', 'gpu'])
def _alter_conv3d_layout(attrs, inputs, tinfos, out_type):
    target = tvm.target.Target.current(allow_none=False)
    dispatch_ctx = autotvm.task.DispatchContext.current
    (_, outs) = relay.backend.te_compiler.select_implementation(relay.op.get('nn.conv3d'), attrs, tinfos, out_type, target)
    workload = autotvm.task.get_workload(outs)
    if workload is None:
        return None
    cfg = dispatch_ctx.query(target, workload)
    if cfg.is_fallback:
        autotvm.task.clear_fallback_cache(target, workload)
        return None
    topi_tmpl = workload[0]
    new_attrs = {k: attrs[k] for k in attrs.keys()}
    strides = attrs.get_int_tuple('strides')
    padding = attrs.get_int_tuple('padding')
    dilation = attrs.get_int_tuple('dilation')
    groups = attrs.get_int('groups')
    data_layout = attrs['data_layout']
    kernel_layout = attrs['kernel_layout']
    (data, kernel) = tinfos
    out_dtype = out_type.dtype
    if topi_tmpl == 'conv3d_ncdhw_winograd.cuda':
        if dilation != (1, 1, 1):
            logger.warning('Does not support weight pre-transform for dilated 3D convolution.')
            return None
        assert data_layout == 'NCDHW' and kernel_layout == 'OIDHW'
        (N, CI, D, H, W) = get_const_tuple(data.shape)
        (CO, _, KD, KH, KW) = get_const_tuple(kernel.shape)
        tile_size = _infer_tile_size(tinfos[0], tinfos[1])
        weight = relay.nn.contrib_conv3d_winograd_weight_transform(inputs[1], tile_size=tile_size)
        new_attrs['tile_size'] = tile_size
        new_attrs['channels'] = CO
        new_data = data
        if 2 < KD < 8 and KD == KH:
            new_weight = te.placeholder((KD + tile_size - 1, KH + tile_size - 1, KW + tile_size - 1, CO, CI), dtype=kernel.dtype)
        else:
            new_weight = te.placeholder((KH + tile_size - 1, KW + tile_size - 1, KD, CO, CI), dtype=kernel.dtype)
        new_workload = autotvm.task.args_to_workload([new_data, new_weight, strides, padding, dilation, out_dtype], 'conv3d_ncdhw_winograd_without_weight_transform.cuda')
        dispatch_ctx.update(target, new_workload, cfg)
        return relay.nn.contrib_conv3d_winograd_without_weight_transform(inputs[0], weight, **new_attrs)
    return None