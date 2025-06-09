def add_cluster_field(self, description):
    """ Adds a field or a list of fields to the cluster result array. Has to be defined as a numpy dtype entry, e.g.: ('parameter', '<i4') """
    if isinstance(description, list):
        for item in description:
            if len(item) != 2:
                raise TypeError('Description needs to be a list of 2-tuples of a string and a dtype.')
            self._cluster_descr.append(item)
    else:
        if len(description) != 2:
            raise TypeError('Description needs to be a 2-tuple of a string and a dtype.')
        self._cluster_descr.append(description)
    self._init_arrays(size=0)