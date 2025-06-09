def import_table(self, table, target_dir=None, append=False, file_type='text', columns=None, split_by=None, where=None, direct=False, driver=None, extra_import_options=None):
    """
        Imports table from remote location to target dir. Arguments are
        copies of direct sqoop command line arguments

        :param table: Table to read
        :param target_dir: HDFS destination dir
        :param append: Append data to an existing dataset in HDFS
        :param file_type: "avro", "sequence", "text" or "parquet".
            Imports data to into the specified format. Defaults to text.
        :param columns: <col,col,col…> Columns to import from table
        :param split_by: Column of the table used to split work units
        :param where: WHERE clause to use during import
        :param direct: Use direct connector if exists for the database
        :param driver: Manually specify JDBC driver class to use
        :param extra_import_options: Extra import options to pass as dict.
            If a key doesn't have a value, just pass an empty string to it.
            Don't include prefix of -- for sqoop options.
        """
    cmd = self._import_cmd(target_dir, append, file_type, split_by, direct, driver, extra_import_options)
    cmd += ['--table', table]
    if columns:
        cmd += ['--columns', columns]
    if where:
        cmd += ['--where', where]
    self.Popen(cmd)