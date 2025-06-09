def _get_stream_id(self, text):
    """Try to find a stream_id"""
    m = self._image_re.search(text)
    if m:
        return m.group('stream_id')