import warnings
import numba
import numpy as np
from aesara.link.numba.dispatch import basic as numba_basic
from aesara.link.numba.dispatch.basic import _numba_funcify, get_numba_type, int_to_float_fn
from aesara.tensor.nlinalg import SVD, Det, Eig, Eigh, Inv, MatrixInverse, MatrixPinv, QRFull

@_numba_funcify.register(SVD)
def numba_funcify_SVD(op, node, **kwargs):
    full_matrices = op.full_matrices
    compute_uv = op.compute_uv
    if not compute_uv:
        warnings.warn('Numba will use object mode to allow the `compute_uv` argument to `numpy.linalg.svd`.', UserWarning)
        ret_sig = get_numba_type(node.outputs[0].type, node.outputs[0])

        @numba_basic.numba_njit
        def svd(x):
            with numba.objmode(ret=ret_sig):
                ret = np.linalg.svd(x, full_matrices, compute_uv)
            return ret
    else:
        out_dtype = node.outputs[0].type.numpy_dtype
        inputs_cast = int_to_float_fn(node.inputs, out_dtype)

        @numba_basic.numba_njit(inline='always')
        def svd(x):
            return np.linalg.svd(inputs_cast(x), full_matrices)
    return svd

@_numba_funcify.register(Det)
def numba_funcify_Det(op, node, **kwargs):
    out_dtype = node.outputs[0].type.numpy_dtype
    inputs_cast = int_to_float_fn(node.inputs, out_dtype)

    @numba_basic.numba_njit(inline='always')
    def det(x):
        return numba_basic.direct_cast(np.linalg.det(inputs_cast(x)), out_dtype)
    return det

@_numba_funcify.register(Eig)
def numba_funcify_Eig(op, node, **kwargs):
    out_dtype_1 = node.outputs[0].type.numpy_dtype
    out_dtype_2 = node.outputs[1].type.numpy_dtype
    inputs_cast = int_to_float_fn(node.inputs, out_dtype_1)

    @numba_basic.numba_njit
    def eig(x):
        out = np.linalg.eig(inputs_cast(x))
        return (out[0].astype(out_dtype_1), out[1].astype(out_dtype_2))
    return eig

@_numba_funcify.register(Eigh)
def numba_funcify_Eigh(op, node, **kwargs):
    uplo = op.UPLO
    if uplo != 'L':
        warnings.warn('Numba will use object mode to allow the `UPLO` argument to `numpy.linalg.eigh`.', UserWarning)
        out_dtypes = tuple((o.type.numpy_dtype for o in node.outputs))
        ret_sig = numba.types.Tuple([get_numba_type(node.outputs[0].type, node.outputs[0]), get_numba_type(node.outputs[1].type, node.outputs[1])])

        @numba_basic.numba_njit
        def eigh(x):
            with numba.objmode(ret=ret_sig):
                out = np.linalg.eigh(x, UPLO=uplo)
                ret = (out[0].astype(out_dtypes[0]), out[1].astype(out_dtypes[1]))
            return ret
    else:

        @numba_basic.numba_njit(inline='always')
        def eigh(x):
            return np.linalg.eigh(x)
    return eigh

@_numba_funcify.register(Inv)
def numba_funcify_Inv(op, node, **kwargs):
    out_dtype = node.outputs[0].type.numpy_dtype
    inputs_cast = int_to_float_fn(node.inputs, out_dtype)

    @numba_basic.numba_njit(inline='always')
    def inv(x):
        return np.linalg.inv(inputs_cast(x)).astype(out_dtype)
    return inv

@_numba_funcify.register(MatrixInverse)
def numba_funcify_MatrixInverse(op, node, **kwargs):
    out_dtype = node.outputs[0].type.numpy_dtype
    inputs_cast = int_to_float_fn(node.inputs, out_dtype)

    @numba_basic.numba_njit(inline='always')
    def matrix_inverse(x):
        return np.linalg.inv(inputs_cast(x)).astype(out_dtype)
    return matrix_inverse

@_numba_funcify.register(MatrixPinv)
def numba_funcify_MatrixPinv(op, node, **kwargs):
    out_dtype = node.outputs[0].type.numpy_dtype
    inputs_cast = int_to_float_fn(node.inputs, out_dtype)

    @numba_basic.numba_njit(inline='always')
    def matrixpinv(x):
        return np.linalg.pinv(inputs_cast(x)).astype(out_dtype)
    return matrixpinv

@_numba_funcify.register(QRFull)
def numba_funcify_QRFull(op, node, **kwargs):
    mode = op.mode
    if mode != 'reduced':
        warnings.warn('Numba will use object mode to allow the `mode` argument to `numpy.linalg.qr`.', UserWarning)
        if len(node.outputs) > 1:
            ret_sig = numba.types.Tuple([get_numba_type(o.type, o) for o in node.outputs])
        else:
            ret_sig = get_numba_type(node.outputs[0].type, node.outputs[0])

        @numba_basic.numba_njit
        def qr_full(x):
            with numba.objmode(ret=ret_sig):
                ret = np.linalg.qr(x, mode=mode)
            return ret
    else:
        out_dtype = node.outputs[0].type.numpy_dtype
        inputs_cast = int_to_float_fn(node.inputs, out_dtype)

        @numba_basic.numba_njit(inline='always')
        def qr_full(x):
            return np.linalg.qr(inputs_cast(x))
    return qr_full