def unpacked_dtype(self):
    """ Returns the numpy.dtype used to store the point records in a numpy array

        .. note::

            The dtype corresponds to the dtype with sub_fields *unpacked*

        """
    dtype = self._access_dict(dims.UNPACKED_POINT_FORMATS_DTYPES, self.id)
    dtype = self._dtype_add_extra_dims(dtype)
    return dtype