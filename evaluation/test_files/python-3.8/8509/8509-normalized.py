def count(self, coordinates):
    """Return number of objects that intersect the given coordinates.

        :param coordinates: sequence or array
            This may be an object that satisfies the numpy array
            protocol, providing the index's dimension * 2 coordinate
            pairs representing the `mink` and `maxk` coordinates in
            each dimension defining the bounds of the query window.

        The following example queries the index for any objects any objects
        that were stored in the index intersect the bounds given in the
        coordinates::

            >>> from rtree import index
            >>> idx = index.Index()
            >>> idx.insert(4321,
            ...            (34.3776829412, 26.7375853734, 49.3776829412,
            ...             41.7375853734),
            ...            obj=42)

            >>> print(idx.count((0, 0, 60, 60)))
            1

        """
    (p_mins, p_maxs) = self.get_coordinate_pointers(coordinates)
    p_num_results = ctypes.c_uint64(0)
    core.rt.Index_Intersects_count(self.handle, p_mins, p_maxs, self.properties.dimension, ctypes.byref(p_num_results))
    return p_num_results.value