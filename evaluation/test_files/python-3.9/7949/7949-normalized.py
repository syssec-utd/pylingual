def zeros(cls, point_format, point_count):
    """ Creates a new point record with all dimensions initialized to zero

        Parameters
        ----------
        point_format_id: int
            The point format id the point record should have
        point_count : int
            The number of point the point record should have

        Returns
        -------
        PackedPointRecord

        """
    data = np.zeros(point_count, point_format.dtype)
    return cls(data, point_format)