def _create_counter_column_family(self, family, counter_columns=[], key_validation_class=UTF8Type):
    """
        Creates a column family of the name 'family' and sets any of
        the names in the bytes_column list to have the BYTES_TYPE.

        key_validation_class defaults to TIME_UUID_TYPE and could also
        be ASCII_TYPE for md5 hash keys, like we use for 'inbound'
        """
    sm = SystemManager(random.choice(self.server_list))
    sm.create_column_family(self.namespace, family, super=False, key_validation_class=key_validation_class, default_validation_class='CounterColumnType', column_name_class=ASCII_TYPE)
    for column in counter_columns:
        sm.alter_column(self.namespace, family, column, COUNTER_COLUMN_TYPE)
    sm.close()