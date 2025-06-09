def get_tables(self, db, pattern='*'):
    """
        Get a metastore table object
        """
    with self.metastore as client:
        tables = client.get_tables(db_name=db, pattern=pattern)
        return client.get_table_objects_by_name(db, tables)