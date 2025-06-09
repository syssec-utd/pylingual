def write_triggers(self, table):
    """Write TRIGGERs existing on `table` to the output file

        :Parameters:
          - `table`: an instance of a :py:class:`mysql2pgsql.lib.mysql_reader.MysqlReader.Table` object that represents the table to read/write.

        Returns None
        """
    self.f.write('\n'.join(super(PostgresFileWriter, self).write_triggers(table)))