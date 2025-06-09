def read_blob(self, blob_dim, n_blob=0):
    """Read blob from a selection.
        """
    n_blobs = self.calc_n_blobs(blob_dim)
    if n_blob > n_blobs or n_blob < 0:
        raise ValueError('Please provide correct n_blob value. Given %i, but max values is %i' % (n_blob, n_blobs))
    if blob_dim[self.time_axis] * (n_blob + 1) > self.selection_shape[self.time_axis]:
        updated_blob_dim = (self.selection_shape[self.time_axis] - blob_dim[self.time_axis] * n_blob, 1, blob_dim[self.freq_axis])
    else:
        updated_blob_dim = [int(i) for i in blob_dim]
    blob_start = self._find_blob_start(blob_dim, n_blob)
    blob_end = blob_start + np.array(updated_blob_dim)
    blob = self.h5['data'][int(blob_start[self.time_axis]):int(blob_end[self.time_axis]), :, int(blob_start[self.freq_axis]):int(blob_end[self.freq_axis])]
    return blob