def detectBOM(self):
    """Attempts to detect at BOM at the start of the stream. If
        an encoding can be determined from the BOM return the name of the
        encoding otherwise return None"""
    bomDict = {codecs.BOM_UTF8: 'utf-8', codecs.BOM_UTF16_LE: 'utf-16-le', codecs.BOM_UTF16_BE: 'utf-16-be', codecs.BOM_UTF32_LE: 'utf-32-le', codecs.BOM_UTF32_BE: 'utf-32-be'}
    string = self.rawStream.read(4)
    assert isinstance(string, bytes)
    encoding = bomDict.get(string[:3])
    seek = 3
    if not encoding:
        encoding = bomDict.get(string)
        seek = 4
        if not encoding:
            encoding = bomDict.get(string[:2])
            seek = 2
    self.rawStream.seek(encoding and seek or 0)
    return encoding