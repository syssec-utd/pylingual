def patch_instance(self, body, instance, project_id=None):
    """
        Updates settings of a Cloud SQL instance.

        Caution: This is not a partial update, so you must include values for
        all the settings that you want to retain.

        :param body: Body required by the Cloud SQL patch API, as described in
            https://cloud.google.com/sql/docs/mysql/admin-api/v1beta4/instances/patch#request-body.
        :type body: dict
        :param instance: Cloud SQL instance ID. This does not include the project ID.
        :type instance: str
        :param project_id: Project ID of the project that contains the instance. If set
            to None or missing, the default project_id from the GCP connection is used.
        :type project_id: str
        :return: None
        """
    response = self.get_conn().instances().patch(project=project_id, instance=instance, body=body).execute(num_retries=self.num_retries)
    operation_name = response['name']
    self._wait_for_operation_to_complete(project_id=project_id, operation_name=operation_name)