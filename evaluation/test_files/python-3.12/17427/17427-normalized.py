def ParseID3v1(data):
    """Parse an ID3v1 tag, returning a list of ID3v2.4 frames."""
    try:
        data = data[data.index(b'TAG'):]
    except ValueError:
        return None
    if 128 < len(data) or len(data) < 124:
        return None
    unpack_fmt = '3s30s30s30s%ds29sBB' % (len(data) - 124)
    try:
        tag, title, artist, album, year, comment, track, genre = unpack(unpack_fmt, data)
    except StructError:
        return None
    if tag != b'TAG':
        return None

    def fix(data):
        return data.split(b'\x00')[0].strip().decode('latin1')
    title, artist, album, year, comment = map(fix, [title, artist, album, year, comment])
    frames = {}
    if title:
        frames['TIT2'] = TIT2(encoding=0, text=title)
    if artist:
        frames['TPE1'] = TPE1(encoding=0, text=[artist])
    if album:
        frames['TALB'] = TALB(encoding=0, text=album)
    if year:
        frames['TDRC'] = TDRC(encoding=0, text=year)
    if comment:
        frames['COMM'] = COMM(encoding=0, lang='eng', desc='ID3v1 Comment', text=comment)
    if track and (track != 32 or data[-3] == b'\x00'[0]):
        frames['TRCK'] = TRCK(encoding=0, text=str(track))
    if genre != 255:
        frames['TCON'] = TCON(encoding=0, text=str(genre))
    return frames