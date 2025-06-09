def _prm_read_shared_data(self, shared_node, instance):
    """Reads shared data and constructs the appropraite class.

        :param shared_node:

            hdf5 node storing the pandas DataFrame

        :param full_name:

            Full name of the parameter or result whose data is to be loaded

        :return:

            Data to load

        """
    try:
        data_type = self._all_get_from_attrs(shared_node, HDF5StorageService.SHARED_DATA_TYPE)
        constructor = shared.FLAG_CLASS_MAPPING[data_type]
        name = shared_node._v_name
        result = constructor(name=name, parent=instance)
        return result
    except:
        self._logger.error('Failed loading `%s` of `%s`.' % (shared_node._v_name, instance.v_full_name))
        raise