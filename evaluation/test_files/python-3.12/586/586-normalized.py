def create_external_table(self, external_project_dataset_table, schema_fields, source_uris, source_format='CSV', autodetect=False, compression='NONE', ignore_unknown_values=False, max_bad_records=0, skip_leading_rows=0, field_delimiter=',', quote_character=None, allow_quoted_newlines=False, allow_jagged_rows=False, src_fmt_configs=None, labels=None):
    """
        Creates a new external table in the dataset with the data in Google
        Cloud Storage. See here:

        https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#resource

        for more details about these parameters.

        :param external_project_dataset_table:
            The dotted ``(<project>.|<project>:)<dataset>.<table>($<partition>)`` BigQuery
            table name to create external table.
            If ``<project>`` is not included, project will be the
            project defined in the connection json.
        :type external_project_dataset_table: str
        :param schema_fields: The schema field list as defined here:
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#resource
        :type schema_fields: list
        :param source_uris: The source Google Cloud
            Storage URI (e.g. gs://some-bucket/some-file.txt). A single wild
            per-object name can be used.
        :type source_uris: list
        :param source_format: File format to export.
        :type source_format: str
        :param autodetect: Try to detect schema and format options automatically.
            Any option specified explicitly will be honored.
        :type autodetect: bool
        :param compression: [Optional] The compression type of the data source.
            Possible values include GZIP and NONE.
            The default value is NONE.
            This setting is ignored for Google Cloud Bigtable,
            Google Cloud Datastore backups and Avro formats.
        :type compression: str
        :param ignore_unknown_values: [Optional] Indicates if BigQuery should allow
            extra values that are not represented in the table schema.
            If true, the extra values are ignored. If false, records with extra columns
            are treated as bad records, and if there are too many bad records, an
            invalid error is returned in the job result.
        :type ignore_unknown_values: bool
        :param max_bad_records: The maximum number of bad records that BigQuery can
            ignore when running the job.
        :type max_bad_records: int
        :param skip_leading_rows: Number of rows to skip when loading from a CSV.
        :type skip_leading_rows: int
        :param field_delimiter: The delimiter to use when loading from a CSV.
        :type field_delimiter: str
        :param quote_character: The value that is used to quote data sections in a CSV
            file.
        :type quote_character: str
        :param allow_quoted_newlines: Whether to allow quoted newlines (true) or not
            (false).
        :type allow_quoted_newlines: bool
        :param allow_jagged_rows: Accept rows that are missing trailing optional columns.
            The missing values are treated as nulls. If false, records with missing
            trailing columns are treated as bad records, and if there are too many bad
            records, an invalid error is returned in the job result. Only applicable when
            soure_format is CSV.
        :type allow_jagged_rows: bool
        :param src_fmt_configs: configure optional fields specific to the source format
        :type src_fmt_configs: dict
        :param labels: a dictionary containing labels for the table, passed to BigQuery
        :type labels: dict
        """
    if src_fmt_configs is None:
        src_fmt_configs = {}
    project_id, dataset_id, external_table_id = _split_tablename(table_input=external_project_dataset_table, default_project_id=self.project_id, var_name='external_project_dataset_table')
    source_format = source_format.upper()
    allowed_formats = ['CSV', 'NEWLINE_DELIMITED_JSON', 'AVRO', 'GOOGLE_SHEETS', 'DATASTORE_BACKUP', 'PARQUET']
    if source_format not in allowed_formats:
        raise ValueError('{0} is not a valid source format. Please use one of the following types: {1}'.format(source_format, allowed_formats))
    compression = compression.upper()
    allowed_compressions = ['NONE', 'GZIP']
    if compression not in allowed_compressions:
        raise ValueError('{0} is not a valid compression format. Please use one of the following types: {1}'.format(compression, allowed_compressions))
    table_resource = {'externalDataConfiguration': {'autodetect': autodetect, 'sourceFormat': source_format, 'sourceUris': source_uris, 'compression': compression, 'ignoreUnknownValues': ignore_unknown_values}, 'tableReference': {'projectId': project_id, 'datasetId': dataset_id, 'tableId': external_table_id}}
    if schema_fields:
        table_resource['externalDataConfiguration'].update({'schema': {'fields': schema_fields}})
    self.log.info('Creating external table: %s', external_project_dataset_table)
    if max_bad_records:
        table_resource['externalDataConfiguration']['maxBadRecords'] = max_bad_records
    if 'skipLeadingRows' not in src_fmt_configs:
        src_fmt_configs['skipLeadingRows'] = skip_leading_rows
    if 'fieldDelimiter' not in src_fmt_configs:
        src_fmt_configs['fieldDelimiter'] = field_delimiter
    if 'quote_character' not in src_fmt_configs:
        src_fmt_configs['quote'] = quote_character
    if 'allowQuotedNewlines' not in src_fmt_configs:
        src_fmt_configs['allowQuotedNewlines'] = allow_quoted_newlines
    if 'allowJaggedRows' not in src_fmt_configs:
        src_fmt_configs['allowJaggedRows'] = allow_jagged_rows
    src_fmt_to_param_mapping = {'CSV': 'csvOptions', 'GOOGLE_SHEETS': 'googleSheetsOptions'}
    src_fmt_to_configs_mapping = {'csvOptions': ['allowJaggedRows', 'allowQuotedNewlines', 'fieldDelimiter', 'skipLeadingRows', 'quote'], 'googleSheetsOptions': ['skipLeadingRows']}
    if source_format in src_fmt_to_param_mapping.keys():
        valid_configs = src_fmt_to_configs_mapping[src_fmt_to_param_mapping[source_format]]
        src_fmt_configs = {k: v for k, v in src_fmt_configs.items() if k in valid_configs}
        table_resource['externalDataConfiguration'][src_fmt_to_param_mapping[source_format]] = src_fmt_configs
    if labels:
        table_resource['labels'] = labels
    try:
        self.service.tables().insert(projectId=project_id, datasetId=dataset_id, body=table_resource).execute(num_retries=self.num_retries)
        self.log.info('External table created successfully: %s', external_project_dataset_table)
    except HttpError as err:
        raise Exception('BigQuery job failed. Error was: {}'.format(err.content))