import sys
from comfy_controlnet_preprocessors.uniformer.mmcv.utils import Registry
CONV_LAYERS = Registry('conv layer', sys.modules[__name__])
NORM_LAYERS = Registry('norm layer', sys.modules[__name__])
ACTIVATION_LAYERS = Registry('activation layer', sys.modules[__name__])
PADDING_LAYERS = Registry('padding layer', sys.modules[__name__])
UPSAMPLE_LAYERS = Registry('upsample layer', sys.modules[__name__])
PLUGIN_LAYERS = Registry('plugin layer', sys.modules[__name__])
DROPOUT_LAYERS = Registry('drop out layers', sys.modules[__name__])
POSITIONAL_ENCODING = Registry('position encoding', sys.modules[__name__])
ATTENTION = Registry('attention', sys.modules[__name__])
FEEDFORWARD_NETWORK = Registry('feed-forward Network', sys.modules[__name__])
TRANSFORMER_LAYER = Registry('transformerLayer', sys.modules[__name__])
TRANSFORMER_LAYER_SEQUENCE = Registry('transformer-layers sequence', sys.modules[__name__])