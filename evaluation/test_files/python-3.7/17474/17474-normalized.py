def RegisterTXXXKey(cls, key, desc):
    """Register a user-defined text frame key.

        Some ID3 tags are stored in TXXX frames, which allow a
        freeform 'description' which acts as a subkey,
        e.g. TXXX:BARCODE.::

            EasyID3.RegisterTXXXKey('barcode', 'BARCODE').
        """
    frameid = 'TXXX:' + desc

    def getter(id3, key):
        return list(id3[frameid])

    def setter(id3, key, value):
        try:
            frame = id3[frameid]
        except KeyError:
            enc = 0
            try:
                for v in value:
                    v.encode('latin_1')
            except UnicodeError:
                enc = 3
            id3.add(mutagen.id3.TXXX(encoding=enc, text=value, desc=desc))
        else:
            frame.text = value

    def deleter(id3, key):
        del id3[frameid]
    cls.RegisterKey(key, getter, setter, deleter)