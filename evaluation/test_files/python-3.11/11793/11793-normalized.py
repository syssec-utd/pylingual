def __get_blob_dimensions(self, chunk_dim):
    """ Sets the blob dimmentions, trying to read around 1024 MiB at a time.
            This is assuming a chunk is about 1 MiB.
        """
    if self.selection_shape[self.freq_axis] > chunk_dim[self.freq_axis] * MAX_BLOB_MB:
        freq_axis_size = self.selection_shape[self.freq_axis]
        time_axis_size = 1
    else:
        freq_axis_size = self.selection_shape[self.freq_axis]
        time_axis_size = np.min([chunk_dim[self.time_axis] * MAX_BLOB_MB * chunk_dim[self.freq_axis] / freq_axis_size, self.selection_shape[self.time_axis]])
    blob_dim = (int(time_axis_size), 1, freq_axis_size)
    return blob_dim