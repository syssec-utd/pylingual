def setup(self):
    """ Initialize the required tables in the database """
    with self._db_conn() as conn:
        for table_defn in self._tables.values():
            conn.execute(table_defn)
    return self