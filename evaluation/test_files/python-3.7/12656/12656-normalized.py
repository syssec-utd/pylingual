def _all_create_or_get_groups(self, key, start_hdf5_group=None):
    """Creates new or follows existing group nodes along a given colon separated `key`.

        :param key:

            Colon separated path along hdf5 file, e.g. `parameters.mobiles.cars`.

        :param start_hdf5_group:

            HDF5 group from where to start, leave `None` for the trajectory group.

        :return:

            Final group node, e.g. group node with name `cars`.

        """
    if start_hdf5_group is None:
        newhdf5_group = self._trajectory_group
    else:
        newhdf5_group = start_hdf5_group
    created = False
    if key == '':
        return (newhdf5_group, created)
    split_key = key.split('.')
    for name in split_key:
        (newhdf5_group, created) = self._all_create_or_get_group(name, newhdf5_group)
    return (newhdf5_group, created)