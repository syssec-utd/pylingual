def get_frame(self, frame_id):
    """Get frame by index.

        Args:
            frame_id (int): Index of the expected frame, 0-based.

        Returns:
            ndarray or None: Return the frame if successful, otherwise None.
        """
    if frame_id < 0 or frame_id >= self._frame_cnt:
        raise IndexError('"frame_id" must be between 0 and {}'.format(self._frame_cnt - 1))
    if frame_id == self._position:
        return self.read()
    if self._cache:
        img = self._cache.get(frame_id)
        if img is not None:
            self._position = frame_id + 1
            return img
    self._set_real_position(frame_id)
    ret, img = self._vcap.read()
    if ret:
        if self._cache:
            self._cache.put(self._position, img)
        self._position += 1
    return img