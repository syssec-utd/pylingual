def load(self, filename, known_frames=None, translate=True, v2_version=4):
    """Load tags from a filename.

        Keyword arguments:

        * filename -- filename to load tag data from
        * known_frames -- dict mapping frame IDs to Frame objects
        * translate -- Update all tags to ID3v2.3/4 internally. If you
                       intend to save, this must be true or you have to
                       call update_to_v23() / update_to_v24() manually.
        * v2_version -- if update_to_v23 or update_to_v24 get called (3 or 4)

        Example of loading a custom frame::

            my_frames = dict(mutagen.id3.Frames)
            class XMYF(Frame): ...
            my_frames["XMYF"] = XMYF
            mutagen.id3.ID3(filename, known_frames=my_frames)
        """
    if not v2_version in (3, 4):
        raise ValueError('Only 3 and 4 possible for v2_version')
    from os.path import getsize
    self.filename = filename
    self.__known_frames = known_frames
    self._fileobj = open(filename, 'rb')
    self.__filesize = getsize(filename)
    try:
        try:
            self._load_header()
        except EOFError:
            self.size = 0
            raise ID3NoHeaderError('%s: too small (%d bytes)' % (filename, self.__filesize))
        except (ID3NoHeaderError, ID3UnsupportedVersionError) as err:
            self.size = 0
            import sys
            stack = sys.exc_info()[2]
            try:
                self._fileobj.seek(-128, 2)
            except EnvironmentError:
                reraise(err, None, stack)
            else:
                frames = ParseID3v1(self._fileobj.read(128))
                if frames is not None:
                    self.version = self._V11
                    for v in frames.values():
                        self.add(v)
                else:
                    reraise(err, None, stack)
        else:
            frames = self.__known_frames
            if frames is None:
                if self._V23 <= self.version:
                    frames = Frames
                elif self._V22 <= self.version:
                    frames = Frames_2_2
            data = self.__fullread(self.size - 10)
            for frame in self.__read_frames(data, frames=frames):
                if isinstance(frame, Frame):
                    self.add(frame)
                else:
                    self.unknown_frames.append(frame)
            self.__unknown_version = self.version
    finally:
        self._fileobj.close()
        del self._fileobj
        del self.__filesize
        if translate:
            if v2_version == 3:
                self.update_to_v23()
            else:
                self.update_to_v24()