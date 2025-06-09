def save(self, filename):
    """Save the metadata to the given filename."""
    values = []
    items = sorted(self.items(), key=MP4Tags.__get_sort_stats)
    for key, value in items:
        info = self.__atoms.get(key[:4], (None, type(self).__render_text))
        try:
            values.append(info[1](self, key, value, *info[2:]))
        except (TypeError, ValueError) as s:
            reraise(MP4MetadataValueError, s, sys.exc_info()[2])
    data = Atom.render(b'ilst', b''.join(values))
    fileobj = open(filename, 'rb+')
    try:
        atoms = Atoms(fileobj)
        try:
            path = atoms.path(b'moov', b'udta', b'meta', b'ilst')
        except KeyError:
            self.__save_new(fileobj, atoms, data)
        else:
            self.__save_existing(fileobj, atoms, path, data)
    finally:
        fileobj.close()