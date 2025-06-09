def create_empty_table(self, project_id, dataset_id, table_id, schema_fields=None, time_partitioning=None, cluster_fields=None, labels=None, view=None, num_retries=None):
    """
        Creates a new, empty table in the dataset.
        To create a view, which is defined by a SQL query, parse a dictionary to 'view' kwarg

        :param project_id: The project to create the table into.
        :type project_id: str
        :param dataset_id: The dataset to create the table into.
        :type dataset_id: str
        :param table_id: The Name of the table to be created.
        :type table_id: str
        :param schema_fields: If set, the schema field list as defined here:
            https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs#configuration.load.schema
        :type schema_fields: list
        :param labels: a dictionary containing labels for the table, passed to BigQuery
        :type labels: dict

        **Example**: ::

            schema_fields=[{"name": "emp_name", "type": "STRING", "mode": "REQUIRED"},
                           {"name": "salary", "type": "INTEGER", "mode": "NULLABLE"}]

        :param time_partitioning: configure optional time partitioning fields i.e.
            partition by field, type and expiration as per API specifications.

            .. seealso::
                https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#timePartitioning
        :type time_partitioning: dict
        :param cluster_fields: [Optional] The fields used for clustering.
            Must be specified with time_partitioning, data in the table will be first
            partitioned and subsequently clustered.
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#clustering.fields
        :type cluster_fields: list
        :param view: [Optional] A dictionary containing definition for the view.
            If set, it will create a view instead of a table:
            https://cloud.google.com/bigquery/docs/reference/rest/v2/tables#view
        :type view: dict

        **Example**: ::

            view = {
                "query": "SELECT * FROM `test-project-id.test_dataset_id.test_table_prefix*` LIMIT 1000",
                "useLegacySql": False
            }

        :return: None
        """
    project_id = project_id if project_id is not None else self.project_id
    table_resource = {'tableReference': {'tableId': table_id}}
    if schema_fields:
        table_resource['schema'] = {'fields': schema_fields}
    if time_partitioning:
        table_resource['timePartitioning'] = time_partitioning
    if cluster_fields:
        table_resource['clustering'] = {'fields': cluster_fields}
    if labels:
        table_resource['labels'] = labels
    if view:
        table_resource['view'] = view
    num_retries = num_retries if num_retries else self.num_retries
    self.log.info('Creating Table %s:%s.%s', project_id, dataset_id, table_id)
    try:
        self.service.tables().insert(projectId=project_id, datasetId=dataset_id, body=table_resource).execute(num_retries=num_retries)
        self.log.info('Table created successfully: %s:%s.%s', project_id, dataset_id, table_id)
    except HttpError as err:
        raise AirflowException('BigQuery job failed. Error was: {}'.format(err.content))