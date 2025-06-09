def hpss_beats(input_file, output_csv):
    """HPSS beat tracking

    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save beat event timestamps as a CSV file
    """
    print('Loading  ', input_file)
    (y, sr) = librosa.load(input_file)
    print('Harmonic-percussive separation ... ')
    y = librosa.effects.percussive(y)
    print('Tracking beats on percussive component')
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP_LENGTH, n_fft=N_FFT, aggregate=np.median)
    (tempo, beats) = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr, hop_length=HOP_LENGTH)
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=HOP_LENGTH)
    print('Saving beats to ', output_csv)
    librosa.output.times_csv(output_csv, beat_times)