def _trj_store_meta_data(self, traj):
    """ Stores general information about the trajectory in the hdf5file.

        The `info` table will contain the name of the trajectory, it's timestamp, a comment,
        the length (aka the number of single runs), and the current version number of pypet.

        Also prepares the desired overview tables and fills the `run` table with dummies.

        """
    descriptiondict = {'name': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_LOCATION_LENGTH, pos=0), 'time': pt.StringCol(len(traj.v_time), pos=1), 'timestamp': pt.FloatCol(pos=3), 'comment': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_COMMENT_LENGTH, pos=4), 'length': pt.IntCol(pos=2), 'version': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_NAME_LENGTH, pos=5), 'python': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_NAME_LENGTH, pos=5)}
    infotable = self._all_get_or_create_table(where=self._overview_group, tablename='info', description=descriptiondict, expectedrows=len(traj))
    insert_dict = self._all_extract_insert_dict(traj, infotable.colnames)
    self._all_add_or_modify_row(traj.v_name, insert_dict, infotable, index=0, flags=(HDF5StorageService.ADD_ROW, HDF5StorageService.MODIFY_ROW))
    rundescription_dict = {'name': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_NAME_LENGTH, pos=1), 'time': pt.StringCol(len(traj.v_time), pos=2), 'timestamp': pt.FloatCol(pos=3), 'idx': pt.IntCol(pos=0), 'completed': pt.IntCol(pos=8), 'parameter_summary': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_COMMENT_LENGTH, pos=6), 'short_environment_hexsha': pt.StringCol(7, pos=7), 'finish_timestamp': pt.FloatCol(pos=4), 'runtime': pt.StringCol(pypetconstants.HDF5_STRCOL_MAX_RUNTIME_LENGTH, pos=5)}
    runtable = self._all_get_or_create_table(where=self._overview_group, tablename='runs', description=rundescription_dict)
    hdf5_description_dict = {'complib': pt.StringCol(7, pos=0), 'complevel': pt.IntCol(pos=1), 'shuffle': pt.BoolCol(pos=2), 'fletcher32': pt.BoolCol(pos=3), 'pandas_format': pt.StringCol(7, pos=4), 'encoding': pt.StringCol(11, pos=5)}
    pos = 7
    for (name, table_name) in HDF5StorageService.NAME_TABLE_MAPPING.items():
        hdf5_description_dict[table_name] = pt.BoolCol(pos=pos)
        pos += 1
    hdf5_description_dict.update({'purge_duplicate_comments': pt.BoolCol(pos=pos + 2), 'results_per_run': pt.IntCol(pos=pos + 3), 'derived_parameters_per_run': pt.IntCol(pos=pos + 4)})
    hdf5table = self._all_get_or_create_table(where=self._overview_group, tablename='hdf5_settings', description=hdf5_description_dict)
    insert_dict = {}
    for attr_name in self.ATTR_LIST:
        insert_dict[attr_name] = getattr(self, attr_name)
    for (attr_name, table_name) in self.NAME_TABLE_MAPPING.items():
        insert_dict[table_name] = getattr(self, attr_name)
    for (attr_name, name) in self.PR_ATTR_NAME_MAPPING.items():
        insert_dict[name] = getattr(self, attr_name)
    self._all_add_or_modify_row(traj.v_name, insert_dict, hdf5table, index=0, flags=(HDF5StorageService.ADD_ROW, HDF5StorageService.MODIFY_ROW))
    actual_rows = runtable.nrows
    self._trj_fill_run_table(traj, actual_rows, len(traj._run_information))
    self._grp_store_group(traj, store_data=pypetconstants.STORE_DATA, with_links=False, recursive=False, _hdf5_group=self._trajectory_group)
    self._trj_store_explorations(traj)
    tostore_tables = []
    for (name, table_name) in HDF5StorageService.NAME_TABLE_MAPPING.items():
        if getattr(self, name):
            tostore_tables.append(table_name)
    self._srvc_make_overview_tables(tostore_tables, traj)