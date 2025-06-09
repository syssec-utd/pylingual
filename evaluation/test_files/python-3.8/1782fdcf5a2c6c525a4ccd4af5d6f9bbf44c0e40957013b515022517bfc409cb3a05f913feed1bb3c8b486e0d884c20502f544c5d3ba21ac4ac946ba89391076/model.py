import tensorflow as tf
from ..fastspeech.model import TFFastSpeechEncoder, TFTacotronPostnet, TFFastSpeechLayer
from ..speechsplit.model import InterpLnr
import numpy as np
import copy

class Encoder_6(tf.keras.layers.Layer):

    def __init__(self, config, hparams, **kwargs):
        super(Encoder_6, self).__init__(name='Encoder_6', **kwargs)
        self.dim_neck_3 = hparams.dim_neck_3
        self.freq_3 = hparams.freq_3
        self.dim_f0 = hparams.dim_f0
        self.dim_enc_3 = hparams.dim_enc_3
        self.dim_emb = hparams.dim_spk_emb
        self.chs_grp = hparams.chs_grp
        self.before_dense_1 = tf.keras.layers.Dense(units=self.dim_enc_3, dtype=tf.float32, name='before_dense_1')
        config_1 = copy.deepcopy(config)
        config_1.hidden_size = self.dim_enc_3
        self.layer_1 = [TFFastSpeechLayer(config_1, name='layer_._{}'.format(i)) for i in range(config_1.num_hidden_layers)]
        self.encoder_dense_1 = tf.keras.layers.Dense(units=self.dim_neck_3, dtype=tf.float32, name='encoder_dense_1')
        self.interp = InterpLnr(hparams)

    def call(self, x, attention_mask, training=True):
        x = self.before_dense_1(x)
        for (no, layer_module) in enumerate(self.layer_1):
            x = layer_module([x, attention_mask], training=training)[0]
            x = self.interp(x, tf.tile([tf.shape(x)[1]], [tf.shape(x)[0]]), training=training)
        x = self.encoder_dense_1(x)
        return x

class Encoder_7(tf.keras.layers.Layer):

    def __init__(self, config, hparams, **kwargs):
        super(Encoder_7, self).__init__(name='Encoder_7', **kwargs)
        self.config = config
        self.dim_neck = hparams.dim_neck
        self.dim_neck_3 = hparams.dim_neck_3
        self.dim_freq = hparams.dim_freq
        self.dim_enc = hparams.dim_enc
        self.dim_enc_3 = hparams.dim_enc_3
        self.before_dense_1 = tf.keras.layers.Dense(units=self.dim_enc, dtype=tf.float32, name='before_dense_1')
        self.before_dense_2 = tf.keras.layers.Dense(units=self.dim_enc_3, dtype=tf.float32, name='before_dense_2')
        config_1 = copy.deepcopy(config)
        config_1.hidden_size = self.dim_enc
        self.layer_1 = [TFFastSpeechLayer(config_1, name='layer_._{}'.format(i)) for i in range(config_1.num_hidden_layers)]
        config_2 = copy.deepcopy(config)
        config_2.hidden_size = self.dim_enc_3
        self.layer_2 = [TFFastSpeechLayer(config_2, name='layer_._{}'.format(i)) for i in range(config_2.num_hidden_layers)]
        self.encoder_dense_1 = tf.keras.layers.Dense(units=self.dim_neck, dtype=tf.float32, name='encoder_dense_1')
        self.encoder_dense_2 = tf.keras.layers.Dense(units=self.dim_neck_3, dtype=tf.float32, name='encoder_dense_2')
        self.interp = InterpLnr(hparams)

    def call(self, x_f0, attention_mask, training=True):
        x = x_f0[:, :, :self.dim_freq]
        f0 = x_f0[:, :, self.dim_freq:]
        x = self.before_dense_1(x)
        f0 = self.before_dense_2(f0)
        seq_length = tf.shape(x_f0)[1]
        for (no, layer_module) in enumerate(self.layer_1):
            x = layer_module([x, attention_mask], training=training)[0]
            f0 = self.layer_2[no]([f0, attention_mask], training=training)[0]
            x_f0 = tf.concat((x, f0), axis=2)
            x_f0 = self.interp(x_f0, tf.tile([tf.shape(x_f0)[1]], [tf.shape(x)[0]]), training=training)
            x = x_f0[:, :, :self.dim_enc]
            f0 = x_f0[:, :, self.dim_enc:]
        x = x_f0[:, :, :self.dim_enc]
        f0 = x_f0[:, :, self.dim_enc:]
        x = self.encoder_dense_1(x)
        f0 = self.encoder_dense_2(f0)
        return (x, f0)

class Encoder_t(tf.keras.layers.Layer):

    def __init__(self, config, hparams, **kwargs):
        super(Encoder_t, self).__init__(name='Encoder_t', **kwargs)
        self.dim_neck_2 = hparams.dim_neck_2
        self.freq_2 = hparams.freq_2
        self.dim_freq = hparams.dim_freq
        self.dim_enc_2 = hparams.dim_enc_2
        self.dim_emb = hparams.dim_spk_emb
        self.chs_grp = hparams.chs_grp
        config = copy.deepcopy(config)
        config.num_hidden_layers = 1
        config.hidden_size = self.dim_enc_2
        self.config = config
        self.before_dense = tf.keras.layers.Dense(units=self.dim_enc_2, dtype=tf.float32, name='before_dense_1')
        self.encoder = TFFastSpeechEncoder(config, name='encoder')
        self.encoder_dense = tf.keras.layers.Dense(units=self.dim_neck_2, dtype=tf.float32, name='encoder_dense')

    def call(self, x, attention_mask, training=True):
        x = self.before_dense(x)
        seq_length = tf.shape(x)[1]
        f = self.encoder([x, attention_mask], training=training)[0]
        return self.encoder_dense(f)

class Decoder_3(tf.keras.layers.Layer):

    def __init__(self, config, hparams, **kwargs):
        super(Decoder_3, self).__init__(name='Decoder_3', **kwargs)
        self.config = config
        self.encoder = TFFastSpeechEncoder(config, name='encoder')
        self.before_dense = tf.keras.layers.Dense(units=config.hidden_size, dtype=tf.float32, name='before_dense_1')
        self.linear_projection = tf.keras.layers.Dense(units=hparams.dim_freq, dtype=tf.float32, name='self.linear_projection')

    def call(self, x, attention_mask, training=True):
        x = self.before_dense(x)
        seq_length = tf.shape(x)[1]
        f = self.encoder([x, attention_mask], training=training)[0]
        return self.linear_projection(f)

class Decoder_4(tf.keras.layers.Layer):

    def __init__(self, config, hparams, **kwargs):
        super(Decoder_4, self).__init__(name='Decoder_4', **kwargs)
        self.config = config
        self.encoder = TFFastSpeechEncoder(config, name='encoder')
        self.before_dense = tf.keras.layers.Dense(units=config.hidden_size, dtype=tf.float32, name='before_dense_1')
        self.linear_projection = tf.keras.layers.Dense(units=hparams.dim_f0, dtype=tf.float32, name='self.linear_projection')

    def call(self, x, attention_mask, training=True):
        x = self.before_dense(x)
        seq_length = tf.shape(x)[1]
        f = self.encoder([x, attention_mask], training=training)[0]
        return self.linear_projection(f)

class Model(tf.keras.Model):

    def __init__(self, config, hparams, **kwargs):
        super(Model, self).__init__(name='speechsplit', **kwargs)
        self.encoder_1 = Encoder_7(config.encoder_self_attention_params, hparams)
        self.encoder_2 = Encoder_t(config.encoder_self_attention_params, hparams)
        self.decoder = Decoder_3(config.decoder_self_attention_params, hparams)
        self.freq = hparams.freq
        self.freq_2 = hparams.freq_2
        self.freq_3 = hparams.freq_3

    def call(self, x_f0, x_org, c_trg, mel_lengths, training=True):
        max_length = tf.cast(tf.reduce_max(mel_lengths), tf.int32)
        attention_mask = tf.sequence_mask(lengths=mel_lengths, maxlen=max_length, dtype=tf.float32)
        attention_mask.set_shape((None, None))
        (codes_x, codes_f0) = self.encoder_1(x_f0, attention_mask, training=training)
        codes_2 = self.encoder_2(x_org, attention_mask, training=training)
        code_exp_1 = codes_x
        code_exp_3 = codes_f0
        code_exp_2 = codes_2
        c_trg = tf.tile(tf.expand_dims(c_trg, 1), (1, tf.shape(x_f0)[1], 1))
        encoder_outputs = tf.concat((code_exp_1, code_exp_2, code_exp_3, c_trg), axis=-1)
        mel_outputs = self.decoder(encoder_outputs, attention_mask, training=training)
        return (codes_x, codes_f0, codes_2, encoder_outputs, mel_outputs)

class Model_F0(tf.keras.Model):

    def __init__(self, config, hparams, **kwargs):
        super(Model_F0, self).__init__(name='speechsplit_f0', **kwargs)
        self.encoder_2 = Encoder_t(config.encoder_self_attention_params, hparams)
        self.encoder_3 = Encoder_6(config.encoder_self_attention_params, hparams)
        self.decoder = Decoder_4(config.decoder_self_attention_params, hparams)
        self.freq_2 = hparams.freq_2
        self.freq_3 = hparams.freq_3

    def call(self, x_org, f0_trg, mel_lengths, training=True):
        max_length = tf.cast(tf.reduce_max(mel_lengths), tf.int32)
        attention_mask = tf.sequence_mask(lengths=mel_lengths, maxlen=max_length, dtype=tf.float32)
        attention_mask.set_shape((None, None))
        codes_2 = self.encoder_2(x_org, attention_mask, training=training)
        code_exp_2 = codes_2
        codes_3 = self.encoder_3(f0_trg, attention_mask, training=training)
        code_exp_3 = codes_3
        self.o = [code_exp_2, code_exp_3]
        encoder_outputs = tf.concat((code_exp_2, code_exp_3), axis=-1)
        mel_outputs = self.decoder(encoder_outputs, attention_mask, training=training)
        return (codes_2, codes_3, encoder_outputs, mel_outputs)