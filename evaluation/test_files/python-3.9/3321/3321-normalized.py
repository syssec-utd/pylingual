def __early_downsample(y, sr, hop_length, res_type, n_octaves, nyquist, filter_cutoff, scale):
    """Perform early downsampling on an audio signal, if it applies."""
    downsample_count = __early_downsample_count(nyquist, filter_cutoff, hop_length, n_octaves)
    if downsample_count > 0 and res_type == 'kaiser_fast':
        downsample_factor = 2 ** downsample_count
        hop_length //= downsample_factor
        if len(y) < downsample_factor:
            raise ParameterError('Input signal length={:d} is too short for {:d}-octave CQT'.format(len(y), n_octaves))
        new_sr = sr / float(downsample_factor)
        y = audio.resample(y, sr, new_sr, res_type=res_type, scale=True)
        if not scale:
            y *= np.sqrt(downsample_factor)
        sr = new_sr
    return (y, sr, hop_length)