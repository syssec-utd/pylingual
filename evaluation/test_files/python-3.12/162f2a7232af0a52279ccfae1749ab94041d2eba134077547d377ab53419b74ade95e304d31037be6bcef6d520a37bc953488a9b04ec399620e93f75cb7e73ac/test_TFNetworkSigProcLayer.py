from __future__ import annotations
import _setup_test_env
import logging
import sys
import os
import os.path
import tensorflow as tf
import numpy as np
import unittest
import contextlib
from returnn.tf.network import *
from returnn.tf.layers.signal_processing import *
from returnn.config import Config
from returnn.util import better_exchook
better_exchook.replace_traceback_format_tb()

@contextlib.contextmanager
def make_scope():
    """
    :rtype: tf.compat.v1.Session
    """
    with tf.Graph().as_default() as graph:
        with tf_compat.v1.Session(graph=graph) as session:
            yield session

def test_melFilterbankLayer():
    with make_scope() as session:
        n_in, n_out = (257, 3)
        layer_name = 'mel_filterbank_layer'
        config = Config()
        config.update({'num_outputs': n_out, 'num_inputs': n_in, 'network': {layer_name: {'class': 'mel_filterbank', 'fft_size': 512, 'nr_of_filters': n_out, 'n_out': n_out, 'is_output_layer': True, 'from': 'data:data'}}})
        network = TFNetwork(config=config, train_flag=True)
        network.construct_from_dict(config.typed_value('network'))
        layer = network.layers[layer_name]
        test_out = session.run(layer.output.placeholder, feed_dict={network.get_extern_data('data').placeholder: np.ones((1, 1, 257))})
        assert np.sum(test_out - np.asarray([28.27923584, 53.10634232, 99.71585846], dtype=np.float32)) < 1e-05

def test_complexLinearProjectionLayer():
    with make_scope() as session:
        n_in, n_out = (514, 128)
        layer_name = 'clp_layer'
        config = Config()
        config.update({'num_outputs': n_out, 'num_inputs': n_in, 'network': {layer_name: {'class': 'complex_linear_projection', 'nr_of_filters': n_out, 'n_out': n_out, 'is_output_layer': True, 'from': 'data:data'}}})
        network = TFNetwork(config=config, train_flag=True)
        network.construct_from_dict(config.typed_value('network'))
        layer = network.layers[layer_name]
        assert isinstance(layer, ComplexLinearProjectionLayer)
        i_r = np.ones((1, n_in // 2))
        i_i = np.ones((1, n_in // 2)) * 0.5
        test_input = np.expand_dims(np.reshape(np.transpose(np.reshape(np.concatenate([i_r, i_i], axis=1), (1, 2, 257)), [0, 2, 1]), (1, 514)), 0)
        test_clp_kernel = np.ones((2, n_in // 2, 128))
        network.initialize_params(session)
        test_clp_output = session.run(layer.output.placeholder, feed_dict={network.get_extern_data('data').placeholder: test_input, layer._clp_kernel: test_clp_kernel})
        assert test_clp_output[0, 0, 0] - 6.00722122 < 1e-05

def test_MultichannelStftLayer():

    def _get_ref_output(time_sig, fft_size, frame_size, frame_shift, window_name, frame_nr, channel_nr):
        import numpy as np
        frame_start = frame_nr * frame_shift
        frame_end = frame_start + frame_size
        frame = time_sig[0, frame_start:frame_end, channel_nr]
        if window_name == 'hanning':
            window = np.hanning(frame_size)
        windowed_frame = window * frame
        out = np.fft.rfft(windowed_frame, fft_size)
        return out

    def test_rfftStftConfig_01():
        with make_scope() as session:
            layer_name = 'stft_layer'
            fft_size = 400
            frame_size = 400
            frame_shift = 160
            window = 'hanning'
            test_input = np.ones((1, 32000, 2), dtype=np.float32)
            config = Config()
            config.update({'num_outputs': int(fft_size / 2) + 1 * test_input.shape[2], 'num_inputs': test_input.shape[2], 'network': {layer_name: {'class': 'multichannel_stft_layer', 'frame_shift': frame_shift, 'frame_size': frame_size, 'window': window, 'fft_size': fft_size, 'use_rfft': True, 'nr_of_channels': 2, 'is_output_layer': True, 'from': 'data:data'}}})
            network = TFNetwork(config=config, train_flag=True)
            network.construct_from_dict(config.typed_value('network'))
            layer = network.layers[layer_name]
            test_output = session.run(layer.output.placeholder, {network.get_extern_data('data').placeholder: test_input})
            ref0 = _get_ref_output(test_input, fft_size, frame_size, frame_shift, window, 0, 0)
            resultDiff = np.abs(test_output[0, 0, 0:int(fft_size / 2) + 1] - ref0)
            assert np.mean(resultDiff) < 0.02
            assert np.max(resultDiff) < 1
            pass
    test_rfftStftConfig_01()

def test_MultichannelMultiResStftLayer():

    def _get_ref_output_single_res(time_sig, fft_size, frame_size, frame_shift, window_name, frame_nr, channel_nr):
        import numpy as np
        frame_start = frame_nr * frame_shift
        frame_end = frame_start + frame_size
        frame = time_sig[0, frame_start:frame_end, channel_nr]
        if window_name == 'hanning':
            window = np.hanning(frame_size)
        windowed_frame = window * frame
        out = np.fft.rfft(windowed_frame, fft_size)
        return out

    def test_stftConfig_single_res_01():
        with make_scope() as session:
            layer_name = 'stft_layer'
            fft_sizes = [400]
            frame_sizes = [400]
            frame_shift = 160
            window = 'hanning'
            test_input = np.ones((1, 32000, 2), dtype=np.float32)
            num_outputs = (int(fft_sizes[0] / 2) + 1) * test_input.shape[2]
            config = Config()
            config.update({'num_outputs': num_outputs, 'num_inputs': test_input.shape[2], 'network': {layer_name: {'class': 'multichannel_multiresolution_stft_layer', 'frame_shift': frame_shift, 'frame_sizes': frame_sizes, 'window': window, 'fft_sizes': fft_sizes, 'use_rfft': True, 'nr_of_channels': 2, 'is_output_layer': True, 'from': 'data:data'}}})
            network = TFNetwork(config=config, train_flag=True)
            network.construct_from_dict(config.typed_value('network'))
            layer = network.layers[layer_name]
            test_output = session.run(layer.output.placeholder, {network.get_extern_data('data').placeholder: test_input})
            ref0 = _get_ref_output_single_res(test_input, fft_sizes[0], frame_sizes[0], frame_shift, window, 0, 0)
            resultDiff = np.abs(test_output[0, 0, 0:int(fft_sizes[0] / 2) + 1] - ref0)
            assert test_output.shape[2] == num_outputs
            assert np.mean(resultDiff) < 0.02
            assert np.max(resultDiff) < 1

    def test_stftConfig_multi_res_01():
        with make_scope() as session:
            layer_name = 'stft_layer'
            fft_sizes = [400, 200]
            frame_sizes = [400, 200]
            frame_shift = 160
            window = 'hanning'
            test_input = np.ones((1, 32000, 2), dtype=np.float32)
            test_input[0, 1000:1100, 1] = np.ones(100, dtype=np.float32) * 0.5
            num_outputs = int(np.sum([(int(fft_size / 2) + 1) * test_input.shape[2] for fft_size in fft_sizes]))
            config = Config()
            config.update({'num_outputs': num_outputs, 'num_inputs': test_input.shape[2], 'network': {layer_name: {'class': 'multichannel_multiresolution_stft_layer', 'frame_shift': frame_shift, 'frame_sizes': frame_sizes, 'window': window, 'fft_sizes': fft_sizes, 'use_rfft': True, 'nr_of_channels': 2, 'is_output_layer': True, 'from': 'data:data'}}})
            network = TFNetwork(config=config, train_flag=True)
            network.construct_from_dict(config.typed_value('network'))
            layer = network.layers[layer_name]
            test_output = session.run(layer.output.placeholder, {network.get_extern_data('data').placeholder: test_input})
            assert test_output.shape[2] == num_outputs
            comparison_frame = 6
            ref00 = _get_ref_output_single_res(test_input, fft_sizes[0], frame_sizes[0], frame_shift, window, comparison_frame, 0)
            ref01 = _get_ref_output_single_res(test_input, fft_sizes[0], frame_sizes[0], frame_shift, window, comparison_frame, 1)
            ref10 = _get_ref_output_single_res(test_input, fft_sizes[1], frame_sizes[1], frame_shift, window, comparison_frame, 0)
            ref11 = _get_ref_output_single_res(test_input, fft_sizes[1], frame_sizes[1], frame_shift, window, comparison_frame, 1)
            ref = np.concatenate([ref00, ref01, ref10, ref11], axis=0)
            resultDiff = np.abs(test_output[0, comparison_frame, :] - ref)
            assert np.mean(resultDiff) < 0.02
            assert np.max(resultDiff) < 1

    def test_stftConfig_multi_res_02():
        with make_scope() as session:
            layer_name = 'stft_layer'
            fft_sizes = [400, 200, 800]
            frame_sizes = [400, 200, 800]
            frame_shift = 160
            window = 'hanning'
            test_input = np.random.normal(0, 0.6, (1, 3200, 2))
            num_outputs = int(np.sum([(int(fft_size / 2) + 1) * test_input.shape[2] for fft_size in fft_sizes]))
            config = Config()
            config.update({'num_outputs': num_outputs, 'num_inputs': test_input.shape[2], 'network': {layer_name: {'class': 'multichannel_multiresolution_stft_layer', 'frame_shift': frame_shift, 'frame_sizes': frame_sizes, 'window': window, 'fft_sizes': fft_sizes, 'use_rfft': True, 'nr_of_channels': 2, 'is_output_layer': True, 'from': 'data:data'}}})
            network = TFNetwork(config=config, train_flag=True)
            network.construct_from_dict(config.typed_value('network'))
            layer = network.layers[layer_name]
            test_output = session.run(layer.output.placeholder, {network.get_extern_data('data').placeholder: test_input})
            assert test_output.shape[2] == num_outputs
            comparison_frame = 6
            ref00 = _get_ref_output_single_res(test_input, fft_sizes[0], frame_sizes[0], frame_shift, window, comparison_frame, 0)
            ref01 = _get_ref_output_single_res(test_input, fft_sizes[0], frame_sizes[0], frame_shift, window, comparison_frame, 1)
            ref10 = _get_ref_output_single_res(test_input, fft_sizes[1], frame_sizes[1], frame_shift, window, comparison_frame, 0)
            ref11 = _get_ref_output_single_res(test_input, fft_sizes[1], frame_sizes[1], frame_shift, window, comparison_frame, 1)
            ref20 = _get_ref_output_single_res(test_input, fft_sizes[2], frame_sizes[2], frame_shift, window, comparison_frame, 0)
            ref21 = _get_ref_output_single_res(test_input, fft_sizes[2], frame_sizes[2], frame_shift, window, comparison_frame, 1)
            ref = np.concatenate([ref00, ref01, ref10, ref11, ref20, ref21], axis=0)
            resultDiff = np.abs(test_output[0, comparison_frame, :] - ref)
            assert np.mean(resultDiff) < 0.06
            assert np.max(resultDiff) < 1
    test_stftConfig_single_res_01()
    test_stftConfig_multi_res_01()
    test_stftConfig_multi_res_02()
if __name__ == '__main__':
    better_exchook.install()
    if len(sys.argv) <= 1:
        for k, v in sorted(globals().items()):
            if k.startswith('test_'):
                print('-' * 40)
                print('Executing: %s' % k)
                try:
                    v()
                except unittest.SkipTest as exc:
                    print('SkipTest:', exc)
                print('-' * 40)
        print('Finished all tests.')
    else:
        assert len(sys.argv) >= 2
        for arg in sys.argv[1:]:
            print('Executing: %s' % arg)
            if arg in globals():
                globals()[arg]()
            else:
                eval(arg)