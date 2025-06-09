def write_table(self, table):
    """Write DDL to create the specified `table`.

        :Parameters:
          - `table`: an instance of a :py:class:`mysql2pgsql.lib.mysql_reader.MysqlReader.Table` object that represents the table to read/write.

        Returns None
        """
    table_sql, serial_key_sql = super(PostgresFileWriter, self).write_table(table)
    if serial_key_sql:
        self.f.write('\n%(serial_key_sql)s\n' % {'serial_key_sql': '\n'.join(serial_key_sql)})
    self.f.write('\n-- Table: %(table_name)s\n%(table_sql)s\n' % {'table_name': table.name, 'table_sql': '\n'.join(table_sql)})