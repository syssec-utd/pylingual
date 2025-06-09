def _tree_create_leaf(self, name, trajectory, hdf5_group):
    """ Creates a new pypet leaf instance.

        Returns the leaf and if it is an explored parameter the length of the range.

        """
    class_name = self._all_get_from_attrs(hdf5_group, HDF5StorageService.CLASS_NAME)
    class_constructor = trajectory._create_class(class_name)
    instance = trajectory._construct_instance(class_constructor, name)
    return instance