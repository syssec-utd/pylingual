def _write_local_schema_file(self, cursor):
    """
        Takes a cursor, and writes the BigQuery schema in .json format for the
        results to a local file system.

        :return: A dictionary where key is a filename to be used as an object
            name in GCS, and values are file handles to local files that
            contains the BigQuery schema fields in .json format.
        """
    schema_str = None
    schema_file_mime_type = 'application/json'
    tmp_schema_file_handle = NamedTemporaryFile(delete=True)
    if self.schema is not None and isinstance(self.schema, string_types):
        schema_str = self.schema.encode('utf-8')
    elif self.schema is not None and isinstance(self.schema, list):
        schema_str = json.dumps(self.schema).encode('utf-8')
    else:
        schema = []
        for field in cursor.description:
            field_name = field[0]
            field_type = self.type_map(field[1])
            if field[6] or field_type == 'TIMESTAMP':
                field_mode = 'NULLABLE'
            else:
                field_mode = 'REQUIRED'
            schema.append({'name': field_name, 'type': field_type, 'mode': field_mode})
        schema_str = json.dumps(schema, sort_keys=True).encode('utf-8')
    tmp_schema_file_handle.write(schema_str)
    self.log.info('Using schema for %s: %s', self.schema_filename, schema_str)
    schema_file_to_upload = {'file_name': self.schema_filename, 'file_handle': tmp_schema_file_handle, 'file_mime_type': schema_file_mime_type}
    return schema_file_to_upload