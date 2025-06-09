def create_empty_dataset(self, dataset_id='', project_id='', dataset_reference=None):
    """
        Create a new empty dataset:
        https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/insert

        :param project_id: The name of the project where we want to create
            an empty a dataset. Don't need to provide, if projectId in dataset_reference.
        :type project_id: str
        :param dataset_id: The id of dataset. Don't need to provide,
            if datasetId in dataset_reference.
        :type dataset_id: str
        :param dataset_reference: Dataset reference that could be provided
            with request body. More info:
            https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets#resource
        :type dataset_reference: dict
        """
    if dataset_reference:
        _validate_value('dataset_reference', dataset_reference, dict)
    else:
        dataset_reference = {}
    if 'datasetReference' not in dataset_reference:
        dataset_reference['datasetReference'] = {}
    if not dataset_reference['datasetReference'].get('datasetId') and (not dataset_id):
        raise ValueError('{} not provided datasetId. Impossible to create dataset')
    dataset_required_params = [(dataset_id, 'datasetId', ''), (project_id, 'projectId', self.project_id)]
    for param_tuple in dataset_required_params:
        param, param_name, param_default = param_tuple
        if param_name not in dataset_reference['datasetReference']:
            if param_default and (not param):
                self.log.info('%s was not specified. Will be used default value %s.', param_name, param_default)
                param = param_default
            dataset_reference['datasetReference'].update({param_name: param})
        elif param:
            _api_resource_configs_duplication_check(param_name, param, dataset_reference['datasetReference'], 'dataset_reference')
    dataset_id = dataset_reference.get('datasetReference').get('datasetId')
    dataset_project_id = dataset_reference.get('datasetReference').get('projectId')
    self.log.info('Creating Dataset: %s in project: %s ', dataset_id, dataset_project_id)
    try:
        self.service.datasets().insert(projectId=dataset_project_id, body=dataset_reference).execute(num_retries=self.num_retries)
        self.log.info('Dataset created successfully: In project %s Dataset %s', dataset_project_id, dataset_id)
    except HttpError as err:
        raise AirflowException('BigQuery job failed. Error was: {}'.format(err.content))