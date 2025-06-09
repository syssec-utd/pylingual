import tensorflow as tf
from .layer import *

def get_generator(generator_inputs, generator_outputs_channels, ngf=64):
    layers = []
    with tf.variable_scope('encoder_1'):
        output = gen_conv(generator_inputs, ngf)
        layers.append(output)
    layer_specs = [ngf * 2, ngf * 4, ngf * 8, ngf * 8, ngf * 8, ngf * 8, ngf * 8]
    for out_channels in layer_specs:
        with tf.variable_scope('encoder_%d' % (len(layers) + 1)):
            rectified = lrelu(layers[-1], 0.2)
            convolved = gen_conv(rectified, out_channels)
            output = batchnorm(convolved)
            layers.append(output)
    layer_specs = [(ngf * 8, 0.5), (ngf * 8, 0.5), (ngf * 8, 0.5), (ngf * 8, 0.0), (ngf * 4, 0.0), (ngf * 2, 0.0), (ngf, 0.0)]
    num_encoder_layers = len(layers)
    for decoder_layer, (out_channels, dropout) in enumerate(layer_specs):
        skip_layer = num_encoder_layers - decoder_layer - 1
        with tf.variable_scope('decoder_%d' % (skip_layer + 1)):
            if decoder_layer == 0:
                input = layers[-1]
            else:
                input = tf.concat([layers[-1], layers[skip_layer]], axis=3)
            rectified = tf.nn.relu(input)
            output = gen_deconv(rectified, out_channels)
            output = batchnorm(output)
            if dropout > 0.0:
                output = tf.nn.dropout(output, keep_prob=1 - dropout)
            layers.append(output)
    with tf.variable_scope('decoder_1'):
        input = tf.concat([layers[-1], layers[0]], axis=3)
        rectified = tf.nn.relu(input)
        output = gen_deconv(rectified, generator_outputs_channels)
        output = tf.tanh(output)
        layers.append(output)
    return layers[-1]