def get_datasets_list(self, project_id=None):
    """
        Method returns full list of BigQuery datasets in the current project

        .. seealso::
            For more information, see:
            https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets/list

        :param project_id: Google Cloud Project for which you
            try to get all datasets
        :type project_id: str
        :return: datasets_list

            Example of returned datasets_list: ::

                   {
                      "kind":"bigquery#dataset",
                      "location":"US",
                      "id":"your-project:dataset_2_test",
                      "datasetReference":{
                         "projectId":"your-project",
                         "datasetId":"dataset_2_test"
                      }
                   },
                   {
                      "kind":"bigquery#dataset",
                      "location":"US",
                      "id":"your-project:dataset_1_test",
                      "datasetReference":{
                         "projectId":"your-project",
                         "datasetId":"dataset_1_test"
                      }
                   }
                ]
        """
    dataset_project_id = project_id if project_id else self.project_id
    try:
        datasets_list = self.service.datasets().list(projectId=dataset_project_id).execute(num_retries=self.num_retries)['datasets']
        self.log.info('Datasets List: %s', datasets_list)
    except HttpError as err:
        raise AirflowException('BigQuery job failed. Error was: {}'.format(err.content))
    return datasets_list