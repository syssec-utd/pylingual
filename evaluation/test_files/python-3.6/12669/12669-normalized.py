def _prm_write_shared_table(self, key, hdf5_group, fullname, **kwargs):
    """Creates a new empty table"""
    first_row = None
    description = None
    if 'first_row' in kwargs:
        first_row = kwargs.pop('first_row')
        if not 'description' in kwargs:
            description = {}
            for colname in first_row:
                data = first_row[colname]
                column = self._all_get_table_col(key, [data], fullname)
                description[colname] = column
    if 'description' in kwargs:
        description = kwargs.pop('description')
    if 'filters' in kwargs:
        filters = kwargs.pop('filters')
    else:
        filters = self._all_get_filters(kwargs)
    table = self._hdf5file.create_table(where=hdf5_group, name=key, description=description, filters=filters, **kwargs)
    table.flush()
    if first_row is not None:
        row = table.row
        for key in description:
            row[key] = first_row[key]
        row.append()
        table.flush()