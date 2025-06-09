import numpy as np
import torch
from torchaudio.compliance.kaldi import mfcc, fbank
from masr.data_utils.audio import AudioSegment

class AudioFeaturizer(object):
    """音频特征器

    :param sample_rate: 用于训练的音频的采样率
    :type sample_rate: int
    :param use_dB_normalization: 是否对音频进行音量归一化
    :type use_dB_normalization: bool
    :param target_dB: 对音频进行音量归一化的音量分贝值
    :type target_dB: float
    :param train: 是否训练使用
    :type train: bool
    """

    def __init__(self, feature_method='fbank', n_mels=80, n_mfcc=40, sample_rate=16000, use_dB_normalization=True, target_dB=-20, train=False):
        self._feature_method = feature_method
        self._target_sample_rate = sample_rate
        self._n_mels = n_mels
        self._n_mfcc = n_mfcc
        self._use_dB_normalization = use_dB_normalization
        self._target_dB = target_dB
        self._train = train

    def featurize(self, audio_segment):
        """从AudioSegment中提取音频特征

        :param audio_segment: Audio segment to extract features from.
        :type audio_segment: AudioSegment
        :return: Spectrogram audio feature in 2darray.
        :rtype: ndarray
        """
        if audio_segment.sample_rate != self._target_sample_rate:
            audio_segment.resample(self._target_sample_rate)
        if self._use_dB_normalization:
            audio_segment.normalize(target_db=self._target_dB)
        if self._feature_method == 'linear':
            samples = audio_segment.samples
            return self._compute_linear(samples=samples, sample_rate=audio_segment.sample_rate)
        elif self._feature_method == 'mfcc':
            samples = audio_segment.to('int16')
            return self._compute_mfcc(samples=samples, sample_rate=audio_segment.sample_rate, n_mels=self._n_mels, n_mfcc=self._n_mfcc, train=self._train)
        elif self._feature_method == 'fbank':
            samples = audio_segment.to('int16')
            return self._compute_fbank(samples=samples, sample_rate=audio_segment.sample_rate, n_mels=self._n_mels, train=self._train)
        else:
            raise Exception('没有{}预处理方法'.format(self._feature_method))

    @staticmethod
    def _compute_linear(samples, sample_rate, frame_shift=10.0, frame_length=20.0, eps=1e-14):
        stride_size = int(0.001 * sample_rate * frame_shift)
        window_size = int(0.001 * sample_rate * frame_length)
        truncate_size = (len(samples) - window_size) % stride_size
        samples = samples[:len(samples) - truncate_size]
        nshape = (window_size, (len(samples) - window_size) // stride_size + 1)
        nstrides = (samples.strides[0], samples.strides[0] * stride_size)
        windows = np.lib.stride_tricks.as_strided(samples, shape=nshape, strides=nstrides)
        assert np.all(windows[:, 1] == samples[stride_size:stride_size + window_size])
        weighting = np.hanning(window_size)[:, None]
        fft = np.fft.rfft(windows * weighting, n=None, axis=0)
        fft = np.absolute(fft)
        fft = fft ** 2
        scale = np.sum(weighting ** 2) * sample_rate
        fft[1:-1, :] *= 2.0 / scale
        fft[(0, -1), :] /= scale
        freqs = float(sample_rate) / window_size * np.arange(fft.shape[0])
        ind = np.where(freqs <= sample_rate / 2)[0][-1] + 1
        linear_feat = np.log(fft[:ind, :] + eps)
        linear_feat = linear_feat.transpose([1, 0])
        return linear_feat

    def _compute_mfcc(self, samples, sample_rate, n_mels=80, n_mfcc=40, frame_shift=10, frame_length=25, dither=0.1, train=False):
        dither = dither if train else 0.0
        waveform = torch.from_numpy(np.expand_dims(samples, 0)).float()
        mfcc_feat = mfcc(waveform, num_mel_bins=n_mels, num_ceps=n_mfcc, frame_length=frame_length, frame_shift=frame_shift, dither=dither, sample_frequency=sample_rate)
        mfcc_feat = mfcc_feat.numpy()
        return mfcc_feat

    def _compute_fbank(self, samples, sample_rate, n_mels=161, frame_shift=10, frame_length=25, dither=0.1, train=False):
        dither = dither if train else 0.0
        waveform = torch.from_numpy(np.expand_dims(samples, 0)).float()
        mat = fbank(waveform, num_mel_bins=n_mels, frame_length=frame_length, frame_shift=frame_shift, dither=dither, sample_frequency=sample_rate)
        fbank_feat = mat.numpy()
        return fbank_feat

    @property
    def feature_dim(self):
        """返回特征大小

        :return: 特征大小
        :rtype: int
        """
        if self._feature_method == 'linear':
            return 161
        elif self._feature_method == 'mfcc':
            return self._n_mfcc
        elif self._feature_method == 'fbank':
            return self._n_mels
        else:
            raise Exception('没有{}预处理方法'.format(self._feature_method))