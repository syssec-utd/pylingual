def write_triggers(self, table):
    """Send DDL to create the specified `table` triggers

        :Parameters:
          - `table`: an instance of a :py:class:`mysql2pgsql.lib.mysql_reader.MysqlReader.Table` object that represents the table to read/write.

        Returns None
        """
    index_sql = super(PostgresDbWriter, self).write_triggers(table)
    for sql in index_sql:
        self.execute(sql)