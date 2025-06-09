def bulk_load(self, table, tmp_file):
    """
        Loads a tab-delimited file into a database table
        """
    self.copy_expert('COPY {table} FROM STDIN'.format(table=table), tmp_file)