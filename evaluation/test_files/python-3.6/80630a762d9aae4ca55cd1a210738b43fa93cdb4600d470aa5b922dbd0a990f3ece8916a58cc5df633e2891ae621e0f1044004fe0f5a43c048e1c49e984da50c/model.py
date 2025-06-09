import gluoncv as gcv
from mxnet import gluon
from utils.tvm import set_env
from tvm import relay
from tvm.relay import quantize as qtz

def get_model(model_name, batch_size, logger, pretrained=True, original=False, qconfig=False):
    gluon_model = gluon.model_zoo.vision.get_model(model_name, pretrained=pretrained)
    img_size = 299 if model_name == 'inceptionv3' else 224
    data_shape = (batch_size, 3, img_size, img_size)
    (mod, params) = relay.frontend.from_mxnet(gluon_model, {'data': data_shape})
    logger.debug('original')
    logger.debug(mod.astext(show_meta_data=False))
    if original:
        return (mod, params)
    with qconfig:
        logger.debug('current quantize config')
        logger.debug(qtz.current_qconfig())
        qfunc = qtz.quantize(mod, params)
        logger.debug('after quantize')
        logger.debug(qfunc.astext(show_meta_data=False))
    return (qfunc, params)