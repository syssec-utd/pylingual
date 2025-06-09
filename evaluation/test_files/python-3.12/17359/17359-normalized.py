def insert_chunk(self, id_):
    """Insert a new chunk at the end of the IFF file"""
    if not isinstance(id_, text_type):
        id_ = id_.decode('ascii')
    if not is_valid_chunk_id(id_):
        raise KeyError('AIFF key must be four ASCII characters.')
    self.__fileobj.seek(self.__next_offset)
    self.__fileobj.write(pack('>4si', id_.ljust(4).encode('ascii'), 0))
    self.__fileobj.seek(self.__next_offset)
    chunk = IFFChunk(self.__fileobj, self[u'FORM'])
    self[u'FORM'].resize(self[u'FORM'].data_size + chunk.size)
    self.__chunks[id_] = chunk
    self.__next_offset = chunk.offset + chunk.size