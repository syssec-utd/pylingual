def read_from(cls, data_stream, num_to_read):
    """ Reads vlrs and parse them if possible from the stream

        Parameters
        ----------
        data_stream : io.BytesIO
                      stream to read from
        num_to_read : int
                      number of vlrs to be read

        Returns
        -------
        pylas.vlrs.vlrlist.VLRList
            List of vlrs

        """
    vlrlist = cls()
    for _ in range(num_to_read):
        raw = RawVLR.read_from(data_stream)
        try:
            vlrlist.append(vlr_factory(raw))
        except UnicodeDecodeError:
            logger.error('Failed to decode VLR: {}'.format(raw))
    return vlrlist