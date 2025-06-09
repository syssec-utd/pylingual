def write_to(self, out_stream, do_compress=False):
    """ writes the data to a stream

        Parameters
        ----------
        out_stream: file object
            the destination stream, implementing the write method
        do_compress: bool, optional, default False
            Flag to indicate if you want the date to be compressed
        """
    self.update_header()
    if self.vlrs.get('ExtraBytesVlr') and (not self.points_data.extra_dimensions_names):
        logger.error('Las contains an ExtraBytesVlr, but no extra bytes were found in the point_record, removing the vlr')
        self.vlrs.extract('ExtraBytesVlr')
    if do_compress:
        laz_vrl = create_laz_vlr(self.points_data)
        self.vlrs.append(known.LasZipVlr(laz_vrl.data()))
        raw_vlrs = vlrlist.RawVLRList.from_list(self.vlrs)
        self.header.offset_to_point_data = self.header.size + raw_vlrs.total_size_in_bytes()
        self.header.point_format_id = uncompressed_id_to_compressed(self.header.point_format_id)
        self.header.number_of_vlr = len(raw_vlrs)
        points_bytes = compress_buffer(np.frombuffer(self.points_data.array, np.uint8), laz_vrl.schema, self.header.offset_to_point_data).tobytes()
    else:
        raw_vlrs = vlrlist.RawVLRList.from_list(self.vlrs)
        self.header.number_of_vlr = len(raw_vlrs)
        self.header.offset_to_point_data = self.header.size + raw_vlrs.total_size_in_bytes()
        points_bytes = self.points_data.raw_bytes()
    self.header.write_to(out_stream)
    self._raise_if_not_expected_pos(out_stream, self.header.size)
    raw_vlrs.write_to(out_stream)
    self._raise_if_not_expected_pos(out_stream, self.header.offset_to_point_data)
    out_stream.write(points_bytes)