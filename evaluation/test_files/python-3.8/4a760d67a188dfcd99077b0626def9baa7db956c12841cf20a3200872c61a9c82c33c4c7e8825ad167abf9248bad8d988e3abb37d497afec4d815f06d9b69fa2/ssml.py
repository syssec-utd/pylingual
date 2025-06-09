class SSML:
    """Converts text to annotated SSML form."""

    def __init__(self, text=None, rate=None, volume=None):
        self.ssml = ''
        self._rate = rate
        self._volume = volume
        if text is not None:
            self.text(text)

    def text(self, text):
        self.ssml = text
        if self._rate is not None or self._volume is not None:
            _prosody = ['prosody']
            if self._rate is not None:
                _prosody.append('rate="{rate}"'.format(rate=self._rate))
            if self._volume is not None:
                _prosody.append('volume="{volume}"'.format(volume=self._volume))
            prosody = '<' + ' '.join(_prosody) + '>'
            self.ssml = prosody + self.ssml + '</prosody>'

    def __str__(self):
        return '<speak>{ssml}</speak>'.format(ssml=self.ssml)

    def __hash__(self):
        return hash(self.ssml)

    def __eq__(self, other):
        return self.ssml == other.ssml