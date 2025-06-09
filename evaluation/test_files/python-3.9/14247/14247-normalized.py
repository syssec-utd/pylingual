def to_file(self, filepath, codec='utf-8', mode='normal'):
    """Write the object to a file.

        :param str filepath: Path of the fil.
        :param str codec: Text encoding.
        :param string mode: Flag to for write mode, possible modes:
            'n'/'normal', 's'/'short' and 'b'/'binary'
        """
    self.tier_num = len(self.tiers)
    if mode in ['binary', 'b']:
        with open(filepath, 'wb') as f:

            def writebstr(s):
                try:
                    bstr = s.encode('ascii')
                except UnicodeError:
                    f.write(b'\xff\xff')
                    bstr = b''.join((struct.pack('>h', ord(c)) for c in s))
                f.write(struct.pack('>h', len(s)))
                f.write(bstr)
            f.write(b'ooBinaryFile\x08TextGrid')
            f.write(struct.pack('>d', self.xmin))
            f.write(struct.pack('>d', self.xmax))
            f.write(b'\x01')
            f.write(struct.pack('>i', self.tier_num))
            for tier in self.tiers:
                f.write(chr(len(tier.tier_type)).encode('ascii'))
                f.write(tier.tier_type.encode('ascii'))
                writebstr(tier.name)
                f.write(struct.pack('>d', tier.xmin))
                f.write(struct.pack('>d', tier.xmax))
                ints = tier.get_all_intervals()
                f.write(struct.pack('>i', len(ints)))
                itier = tier.tier_type == 'IntervalTier'
                for c in ints:
                    f.write(struct.pack('>d', c[0]))
                    itier and f.write(struct.pack('>d', c[1]))
                    writebstr(c[2 if itier else 1])
    elif mode in ['normal', 'n', 'short', 's']:
        with codecs.open(filepath, 'w', codec) as f:
            short = mode[0] == 's'

            def wrt(indent, prefix, value, ff=''):
                indent = 0 if short else indent
                prefix = '' if short else prefix
                if value is not None or not short:
                    s = u'{{}}{{}}{}\n'.format(ff)
                    f.write(s.format(' ' * indent, prefix, value))
            f.write(u'File type = "ooTextFile"\nObject class = "TextGrid"\n\n')
            wrt(0, u'xmin = ', self.xmin, '{:f}')
            wrt(0, u'xmax = ', self.xmax, '{:f}')
            wrt(0, u'tiers? ', u'<exists>', '{}')
            wrt(0, u'size = ', self.tier_num, '{:d}')
            wrt(0, u'item []:', None)
            for (tnum, tier) in enumerate(self.tiers, 1):
                wrt(4, u'item [{:d}]:'.format(tnum), None)
                wrt(8, u'class = ', tier.tier_type, '"{}"')
                wrt(8, u'name = ', tier.name, '"{}"')
                wrt(8, u'xmin = ', tier.xmin, '{:f}')
                wrt(8, u'xmax = ', tier.xmax, '{:f}')
                if tier.tier_type == 'IntervalTier':
                    ints = tier.get_all_intervals()
                    wrt(8, u'intervals: size = ', len(ints), '{:d}')
                    for (i, c) in enumerate(ints):
                        wrt(8, 'intervals [{:d}]:'.format(i + 1), None)
                        wrt(12, 'xmin = ', c[0], '{:f}')
                        wrt(12, 'xmax = ', c[1], '{:f}')
                        wrt(12, 'text = ', c[2].replace('"', '""'), '"{}"')
                elif tier.tier_type == 'TextTier':
                    wrt(8, u'points: size = ', len(tier.intervals), '{:d}')
                    for (i, c) in enumerate(tier.get_intervals()):
                        wrt(8, 'points [{:d}]:'.format(i + 1), None)
                        wrt(12, 'number = ', c[0], '{:f}')
                        wrt(12, 'mark = ', c[1].replace('"', '""'), '"{}"')
    else:
        raise Exception('Unknown mode')