def _prm_store_parameter_or_result(self, instance, store_data=pypetconstants.STORE_DATA, store_flags=None, overwrite=None, with_links=False, recursive=False, _hdf5_group=None, _newly_created=False, **kwargs):
    """Stores a parameter or result to hdf5.

        :param instance:

            The instance to be stored

        :param store_data:

            How to store data

        :param store_flags:

            Dictionary containing how to store individual data, usually empty.

        :param overwrite:

            Instructions how to overwrite data

        :param with_links:

            Placeholder because leaves have no links

        :param recursive:

            Placeholder, because leaves have no children

        :param _hdf5_group:

            The hdf5 group for storing the parameter or result

        :param _newly_created:

            If should be created in a new form

        """
    if store_data == pypetconstants.STORE_NOTHING:
        return
    elif store_data == pypetconstants.STORE_DATA_SKIPPING and instance._stored:
        self._logger.debug('Already found `%s` on disk I will not store it!' % instance.v_full_name)
        return
    elif store_data == pypetconstants.OVERWRITE_DATA:
        if not overwrite:
            overwrite = True
    fullname = instance.v_full_name
    self._logger.debug('Storing `%s`.' % fullname)
    if _hdf5_group is None:
        _hdf5_group, _newly_created = self._all_create_or_get_groups(fullname)
    store_dict = {}
    if store_flags is None:
        store_flags = {}
    try:
        if not instance.f_is_empty():
            store_dict = instance._store()
        try:
            instance_flags = instance._store_flags().copy()
        except AttributeError:
            instance_flags = {}
        instance_flags.update(store_flags)
        store_flags = instance_flags
        self._prm_extract_missing_flags(store_dict, store_flags)
        if overwrite:
            if isinstance(overwrite, str):
                overwrite = [overwrite]
            if overwrite is True:
                to_delete = [key for key in store_dict.keys() if key in _hdf5_group]
                self._all_delete_parameter_or_result_or_group(instance, delete_only=to_delete, _hdf5_group=_hdf5_group)
            elif isinstance(overwrite, (list, tuple)):
                overwrite_set = set(overwrite)
                key_set = set(store_dict.keys())
                stuff_not_to_be_overwritten = overwrite_set - key_set
                if overwrite != 'v_annotations' and len(stuff_not_to_be_overwritten) > 0:
                    self._logger.warning('Cannot overwrite `%s`, these items are not supposed to be stored by the leaf node.' % str(stuff_not_to_be_overwritten))
                stuff_to_overwrite = overwrite_set & key_set
                if len(stuff_to_overwrite) > 0:
                    self._all_delete_parameter_or_result_or_group(instance, delete_only=list(stuff_to_overwrite))
            else:
                raise ValueError('Your value of overwrite `%s` is not understood. Please pass `True` of a list of strings to fine grain overwriting.' % str(overwrite))
        self._prm_store_from_dict(fullname, store_dict, _hdf5_group, store_flags, kwargs)
        self._ann_store_annotations(instance, _hdf5_group, overwrite=overwrite)
        if _newly_created or overwrite is True:
            self._prm_add_meta_info(instance, _hdf5_group, overwrite=not _newly_created)
        instance._stored = True
        self._node_processing_timer.signal_update()
    except:
        self._logger.error('Failed storing leaf `%s`. I will remove the hdf5 data I added  again.' % fullname)
        for key in store_dict.keys():
            if key in _hdf5_group:
                hdf5_child = _hdf5_group._f_get_child(key)
                hdf5_child._f_remove(recursive=True)
        if _hdf5_group._v_nchildren == 0:
            _hdf5_group._f_remove(recursive=True)
        raise