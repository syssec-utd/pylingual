import torch
import math
import torch.nn as nn
from .functional import stft, complex_norm, create_mel_filter, phase_vocoder, apply_filterbank, amplitude_to_db, db_to_amplitude, mu_law_encoding, mu_law_decoding

class _ModuleNoStateBuffers(nn.Module):
    """
    Extension of nn.Module that removes buffers
    from state_dict.
    """

    def state_dict(self, destination=None, prefix='', keep_vars=False):
        ret = super(_ModuleNoStateBuffers, self).state_dict(destination, prefix, keep_vars)
        for k in self._buffers:
            del ret[prefix + k]
        return ret

    def _load_from_state_dict(self, state_dict, prefix, *args, **kwargs):
        buffers = self._buffers
        self._buffers = {}
        result = super(_ModuleNoStateBuffers, self)._load_from_state_dict(state_dict, prefix, *args, **kwargs)
        self._buffers = buffers
        return result

class STFT(_ModuleNoStateBuffers):
    """Compute a short-time Fourier transform of the input waveform(s).
    It essentially wraps `torch.stft` but after reshaping the input audio
    to allow for `waveforms` that `.dim()` >= 3.
    It follows most of the `torch.stft` default value, but for `window`,
    if it's not specified (`None`), it uses hann window.

    Args:
        fft_length (int): FFT size [sample]
        hop_length (int): Hop size [sample] between STFT frames.
            Defaults to `fft_length // 4` (75%-overlapping windows) by `torch.stft`.
        win_length (int): Size of STFT window.
            Defaults to `fft_length` by `torch.stft`.
        window (Tensor): 1-D Tensor.
            Defaults to Hann Window of size `win_length` *unlike* `torch.stft`.
        center (bool): Whether to pad `waveforms` on both sides so that the
            `t`-th frame is centered at time `t * hop_length`.
            Defaults to `True` by `torch.stft`.
        pad_mode (str): padding method (see `torch.nn.functional.pad`).
            Defaults to `'reflect'` by `torch.stft`.
        normalized (bool): Whether the results are normalized.
            Defaults to `False` by `torch.stft`.
        onesided (bool): Whether the half + 1 frequency bins are returned to remove
            the symmetric part of STFT of real-valued signal.
            Defaults to `True` by `torch.stft`.
    """

    def __init__(self, fft_length, hop_length=None, win_length=None, window=None, center=True, pad_mode='reflect', normalized=False, onesided=True):
        super(STFT, self).__init__()
        self.fft_length = fft_length
        self.hop_length = hop_length
        self.win_length = win_length
        self.center = center
        self.pad_mode = pad_mode
        self.normalized = normalized
        self.onesided = onesided
        if window is None:
            if win_length is None:
                window = torch.hann_window(fft_length)
            else:
                window = torch.hann_window(win_length)
        self.register_buffer('window', window)

    def forward(self, waveforms):
        """
        Args:
            waveforms (Tensor): Tensor of audio signal of size `(*, channel, time)`

        Returns:
            complex_specgrams (Tensor): `(*, channel, num_freqs, time, complex=2)`
        """
        complex_specgrams = stft(waveforms, self.fft_length, hop_length=self.hop_length, win_length=self.win_length, window=self.window, center=self.center, pad_mode=self.pad_mode, normalized=self.normalized, onesided=self.onesided)
        return complex_specgrams

    def __repr__(self):
        param_str1 = '(fft_length={}, hop_length={}, win_length={})'.format(self.fft_length, self.hop_length, self.win_length)
        param_str2 = '(center={}, pad_mode={}, normalized={}, onesided={})'.format(self.center, self.pad_mode, self.normalized, self.onesided)
        return self.__class__.__name__ + param_str1 + param_str2

class ComplexNorm(nn.Module):
    """Compute the norm of complex tensor input

    Args:
        power (float): Power of the norm. Defaults to `1.0`.

    """

    def __init__(self, power=1.0):
        super(ComplexNorm, self).__init__()
        self.power = power

    def forward(self, complex_tensor):
        """
        Args:
            complex_tensor (Tensor): Tensor shape of `(*, complex=2)`

        Returns:
            Tensor: norm of the input tensor, shape of `(*, )`
        """
        return complex_norm(complex_tensor, self.power)

    def __repr__(self):
        return self.__class__.__name__ + '(power={})'.format(self.power)

class ApplyFilterbank(_ModuleNoStateBuffers):
    """
    Applies a filterbank transform.
    """

    def __init__(self, filterbank):
        super(ApplyFilterbank, self).__init__()
        self.register_buffer('filterbank', filterbank)

    def forward(self, mag_specgrams):
        """
        Args:
            mag_specgrams (Tensor): (channel, time, freq) or (batch, channel, time, freq).

        Returns:
            (Tensor): freq -> filterbank.size(0)
        """
        return apply_filterbank(mag_specgrams, self.filterbank)

class Filterbank(object):
    """
    Base class for providing a filterbank matrix.
    """

    def __init__(self):
        super(Filterbank, self).__init__()

    def get_filterbank(self):
        raise NotImplementedError

class MelFilterbank(Filterbank):
    """
    Provides a filterbank matrix to convert a spectrogram into a mel frequency spectrogram.

    Args:
        num_freqs (int, optional): number of filter banks from stft.
            Defaults to 2048//2 + 1.
        num_mels (int): number of mel bins. Defaults to 128.
        min_freq (float): minimum frequency. Defaults to 0.
        max_freq (float, optional): maximum frequency. Defaults to sample_rate // 2.
        sample_rate (int): sample rate of audio signal. Defaults to None.
        htk (bool, optional): use HTK formula instead of Slaney. Defaults to False.
    """

    def __init__(self, num_freqs=1025, num_mels=128, min_freq=0.0, max_freq=None, sample_rate=None, htk=False):
        super(MelFilterbank, self).__init__()
        if sample_rate is None and max_freq is None:
            raise ValueError('Either max_freq or sample_rate should be specified., but both are None.')
        self.num_freqs = num_freqs
        self.num_mels = num_mels
        self.min_freq = min_freq
        self.max_freq = max_freq if max_freq else sample_rate // 2
        self.htk = htk

    def get_filterbank(self):
        return create_mel_filter(num_freqs=self.num_freqs, num_mels=self.num_mels, min_freq=self.min_freq, max_freq=self.max_freq, htk=self.htk)

    def __repr__(self):
        param_str1 = '(num_freqs={}, snum_mels={}'.format(self.num_freqs, self.num_mels)
        param_str2 = ', min_freq={}, max_freq={})'.format(self.min_freq, self.max_freq)
        param_str3 = ', htk={}'.format(self.htk)
        return self.__class__.__name__ + param_str1 + param_str2 + param_str3

class TimeStretch(_ModuleNoStateBuffers):
    """
    Stretch stft in time without modifying pitch for a given rate.

    Args:

        hop_length (int): Number audio of frames between STFT columns.
        num_freqs (int, optional): number of filter banks from stft.
        fixed_rate (float): rate to speed up or slow down by.
            Defaults to None (in which case a rate must be
            passed to the forward method per batch).
    """

    def __init__(self, hop_length, num_freqs, fixed_rate=None):
        super(TimeStretch, self).__init__()
        self.fixed_rate = fixed_rate
        phase_advance = torch.linspace(0, math.pi * hop_length, num_freqs)[..., None]
        self.register_buffer('phase_advance', phase_advance)

    def forward(self, complex_specgrams, overriding_rate=None):
        """

        Args:
            complex_specgrams (Tensor): complex spectrogram
                (*, channel, freq, time, complex=2)
            overriding_rate (float or None): speed up to apply to this batch.
                If no rate is passed, use self.fixed_rate.

        Returns:
            (Tensor): (*, channel, num_freqs, ceil(time/rate), complex=2)
        """
        if overriding_rate is None:
            rate = self.fixed_rate
            if rate is None:
                raise ValueError('If no fixed_rate is specified, must pass a valid rate to the forward method.')
        else:
            rate = overriding_rate
        if rate == 1.0:
            return complex_specgrams
        return phase_vocoder(complex_specgrams, rate, self.phase_advance)

    def __repr__(self):
        param_str = '(fixed_rate={})'.format(self.fixed_rate)
        return self.__class__.__name__ + param_str

def Spectrogram(fft_length, hop_length=None, win_length=None, window=None, center=True, pad_mode='reflect', normalized=False, onesided=True, power=1.0):
    """Get spectrogram module, which is a Sequential module of
        `[STFT(), ComplexNorm()]`.

    Args:
        fft_length (int): FFT size [sample]
        hop_length (int): Hop size [sample] between STFT frames.
            Defaults to `fft_length // 4` (75%-overlapping windows) by `torch.stft`.
        win_length (int): Size of STFT window.
            Defaults to `fft_length` by `torch.stft`.
        window (Tensor): 1-D Tensor.
            Defaults to Hann Window of size `win_length` *unlike* `torch.stft`.
        center (bool): Whether to pad `waveforms` on both sides so that the
            `t`-th frame is centered at time `t * hop_length`.
            Defaults to `True` by `torch.stft`.
        pad_mode (str): padding method (see `torch.nn.functional.pad`).
            Defaults to `'reflect'` by `torch.stft`.
        normalized (bool): Whether the results are normalized.
            Defaults to `False` by `torch.stft`.
        onesided (bool): Whether the half + 1 frequency bins are returned to remove
            the symmetric part of STFT of real-valued signal.
            Defaults to `True` by `torch.stft`.
        power (float): Exponent of the magnitude. Defaults to `1.0`.

    """
    return nn.Sequential(STFT(fft_length, hop_length, win_length, window, center, pad_mode, normalized, onesided), ComplexNorm(power))

def Melspectrogram(num_mels=128, sample_rate=22050, min_freq=0.0, max_freq=None, num_freqs=None, htk=False, mel_filterbank=None, **kwargs):
    """
    Get melspectrogram module.

    Args:
        num_mels (int): number of mel bins. Defaults to 128.
        sample_rate (int): sample rate of audio signal. Defaults to 22050.
        min_freq (float): minimum frequency. Defaults to 0.
        max_freq (float, optional): maximum frequency. Defaults to sample_rate // 2.
        num_freqs (int, optional): number of filter banks from stft.
            Defaults to fft_len//2 + 1 if 'fft_len' in kwargs else 1025.
        htk (bool, optional): use HTK formula instead of Slaney. Defaults to False.
        mel_filterbank (class, optional): MelFilterbank class to build filterbank matrix
        **kwargs: torchaudio_contrib.Spectrogram parameters.
    """
    fft_length = kwargs.get('fft_length', None)
    num_freqs = fft_length // 2 + 1 if fft_length else 1025
    if mel_filterbank is None:
        mel_filterbank = MelFilterbank
    mel_fb_matrix = mel_filterbank(num_mels=num_mels, sample_rate=sample_rate, min_freq=min_freq, max_freq=max_freq, num_freqs=num_freqs, htk=htk).get_filterbank()
    return nn.Sequential(*Spectrogram(power=2.0, **kwargs), ApplyFilterbank(mel_fb_matrix))

class AmplitudeToDb(_ModuleNoStateBuffers):
    """
    Amplitude-to-decibel conversion (logarithmic mapping with base=10)
    By using `amin=1e-7`, it assumes 32-bit floating point input. If the
    data precision differs, use approproate `amin` accordingly.

    Args:
        ref (float): Amplitude value that is equivalent to 0 decibel
        amin (float): Minimum amplitude. Any input that is smaller than `amin` is
            clamped to `amin`.
    """

    def __init__(self, ref=1.0, amin=1e-07):
        super(AmplitudeToDb, self).__init__()
        self.ref = ref
        self.amin = amin
        assert ref > amin, 'Reference value is expected to be bigger than amin, but I haveref:{} and amin:{}'.format(ref, amin)

    def forward(self, x):
        """
        Args:
            x (Tensor): Input amplitude

        Returns:
            (Tensor): same size of x, after conversion
        """
        return amplitude_to_db(x, ref=self.ref, amin=self.amin)

    def __repr__(self):
        param_str = '(ref={}, amin={})'.format(self.ref, self.amin)
        return self.__class__.__name__ + param_str

class DbToAmplitude(_ModuleNoStateBuffers):
    """
    Decibel-to-amplitude conversion (exponential mapping with base=10)

    Args:
        x (Tensor): Input in decibel to be converted
        ref (float): Amplitude value that is equivalent to 0 decibel

    Returns:
        (Tensor): same size of x, after conversion
    """

    def __init__(self, ref=1.0):
        super(DbToAmplitude, self).__init__()
        self.ref = ref

    def forward(self, x):
        """
        Args:
            x (Tensor): Input in decibel to be converted

        Returns:
            (Tensor): same size of x, after conversion
        """
        return db_to_amplitude(x, ref=self.ref)

    def __repr__(self):
        param_str = '(ref={})'.format(self.ref)
        return self.__class__.__name__ + param_str

class MuLawEncoding(_ModuleNoStateBuffers):
    """Apply mu-law encoding to the input tensor.
    Usually applied to waveforms

    Args:
        n_quantize (int): quantization level. For 8-bit encoding, set 256 (2 ** 8).

    """

    def __init__(self, n_quantize=256):
        super(MuLawEncoding, self).__init__()
        self.n_quantize = n_quantize

    def forward(self, x):
        """
        Args:
            x (Tensor): input value

        Returns:
            (Tensor): same size of x, after encoding
        """
        return mu_law_encoding(x, self.n_quantize)

    def __repr__(self):
        param_str = '(n_quantize={})'.format(self.n_quantize)
        return self.__class__.__name__ + param_str

class MuLawDecoding(_ModuleNoStateBuffers):
    """Apply mu-law decoding (expansion) to the input tensor.
    Usually applied to waveforms

    Args:
        n_quantize (int): quantization level. For 8-bit decoding, set 256 (2 ** 8).
    """

    def __init__(self, n_quantize=256):
        super(MuLawDecoding, self).__init__()
        self.n_quantize = n_quantize

    def forward(self, x_mu):
        """
        Args:
            x_mu (Tensor): mu-law encoded input

        Returns:
            (Tensor): mu-law decoded tensor
        """
        return mu_law_decoding(x_mu, self.n_quantize)

    def __repr__(self):
        param_str = '(n_quantize={})'.format(self.n_quantize)
        return self.__class__.__name__ + param_str