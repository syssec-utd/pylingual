def _compute_framesync_times(self):
    """Computes the framesync times based on the framesync features."""
    self._framesync_times = librosa.core.frames_to_time(np.arange(self._framesync_features.shape[0]), self.sr, self.hop_length)