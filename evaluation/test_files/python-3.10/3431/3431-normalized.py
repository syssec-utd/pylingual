def clicks(times=None, frames=None, sr=22050, hop_length=512, click_freq=1000.0, click_duration=0.1, click=None, length=None):
    """Returns a signal with the signal `click` placed at each specified time

    Parameters
    ----------
    times : np.ndarray or None
        times to place clicks, in seconds

    frames : np.ndarray or None
        frame indices to place clicks

    sr : number > 0
        desired sampling rate of the output signal

    hop_length : int > 0
        if positions are specified by `frames`, the number of samples between frames.

    click_freq : float > 0
        frequency (in Hz) of the default click signal.  Default is 1KHz.

    click_duration : float > 0
        duration (in seconds) of the default click signal.  Default is 100ms.

    click : np.ndarray or None
        optional click signal sample to use instead of the default blip.

    length : int > 0
        desired number of samples in the output signal


    Returns
    -------
    click_signal : np.ndarray
        Synthesized click signal


    Raises
    ------
    ParameterError
        - If neither `times` nor `frames` are provided.
        - If any of `click_freq`, `click_duration`, or `length` are out of range.


    Examples
    --------
    >>> # Sonify detected beat events
    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    >>> y_beats = librosa.clicks(frames=beats, sr=sr)

    >>> # Or generate a signal of the same length as y
    >>> y_beats = librosa.clicks(frames=beats, sr=sr, length=len(y))

    >>> # Or use timing instead of frame indices
    >>> times = librosa.frames_to_time(beats, sr=sr)
    >>> y_beat_times = librosa.clicks(times=times, sr=sr)

    >>> # Or with a click frequency of 880Hz and a 500ms sample
    >>> y_beat_times880 = librosa.clicks(times=times, sr=sr,
    ...                                  click_freq=880, click_duration=0.5)

    Display click waveform next to the spectrogram

    >>> import matplotlib.pyplot as plt
    >>> plt.figure()
    >>> S = librosa.feature.melspectrogram(y=y, sr=sr)
    >>> ax = plt.subplot(2,1,2)
    >>> librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
    ...                          x_axis='time', y_axis='mel')
    >>> plt.subplot(2,1,1, sharex=ax)
    >>> librosa.display.waveplot(y_beat_times, sr=sr, label='Beat clicks')
    >>> plt.legend()
    >>> plt.xlim(15, 30)
    >>> plt.tight_layout()
    """
    if times is None:
        if frames is None:
            raise ParameterError('either "times" or "frames" must be provided')
        positions = frames_to_samples(frames, hop_length=hop_length)
    else:
        positions = time_to_samples(times, sr=sr)
    if click is not None:
        util.valid_audio(click, mono=True)
    else:
        if click_duration <= 0:
            raise ParameterError('click_duration must be strictly positive')
        if click_freq <= 0:
            raise ParameterError('click_freq must be strictly positive')
        angular_freq = 2 * np.pi * click_freq / float(sr)
        click = np.logspace(0, -10, num=int(np.round(sr * click_duration)), base=2.0)
        click *= np.sin(angular_freq * np.arange(len(click)))
    if length is None:
        length = positions.max() + click.shape[0]
    else:
        if length < 1:
            raise ParameterError('length must be a positive integer')
        positions = positions[positions < length]
    click_signal = np.zeros(length, dtype=np.float32)
    for start in positions:
        end = start + click.shape[0]
        if end >= length:
            click_signal[start:] += click[:length - start]
        else:
            click_signal[start:end] += click
    return click_signal