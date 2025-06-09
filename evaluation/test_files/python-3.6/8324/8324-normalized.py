def write_indexes(self, table):
    """Send DDL to create the specified `table` indexes

        :Parameters:
          - `table`: an instance of a :py:class:`mysql2pgsql.lib.mysql_reader.MysqlReader.Table` object that represents the table to read/write.

        Returns None
        """
    index_sql = super(PostgresDbWriter, self).write_indexes(table)
    for sql in index_sql:
        self.execute(sql)