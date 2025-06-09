def f_backup(self, **kwargs):
    """Backs up the trajectory with the given storage service.

        Arguments of ``kwargs`` are directly passed to the storage service,
        for the HDF5StorageService you can provide the following argument:

        :param backup_filename:

            Name of file where to store the backup.

            In case you use the standard HDF5 storage service and `backup_filename=None`,
            the file will be chosen automatically.
            The backup file will be in the same folder as your hdf5 file and
            named 'backup_XXXXX.hdf5' where 'XXXXX' is the name of your current trajectory.

        """
    self._storage_service.store(pypetconstants.BACKUP, self, trajectory_name=self.v_name, **kwargs)