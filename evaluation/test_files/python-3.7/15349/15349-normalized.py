def fetch_table_names(self, include_system_table=False):
    """
        :return: List of table names in the database.
        :rtype: list
        """
    result = self.__cur.execute("SELECT name FROM sqlite_master WHERE TYPE='table'")
    if result is None:
        return []
    table_names = [record[0] for record in result.fetchall()]
    if include_system_table:
        return table_names
    return [table for table in table_names if table not in SQLITE_SYSTEM_TABLES]