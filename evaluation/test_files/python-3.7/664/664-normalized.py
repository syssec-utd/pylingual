def get_table(self, database_name, table_name):
    """
        Get the information of the table

        :param database_name: Name of hive database (schema) @table belongs to
        :type database_name: str
        :param table_name: Name of hive table
        :type table_name: str
        :rtype: dict

        >>> hook = AwsGlueCatalogHook()
        >>> r = hook.get_table('db', 'table_foo')
        >>> r['Name'] = 'table_foo'
        """
    result = self.get_conn().get_table(DatabaseName=database_name, Name=table_name)
    return result['Table']