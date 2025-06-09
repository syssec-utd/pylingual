def create_database(self, instance_id, database_id, ddl_statements, project_id=None):
    """
        Creates a new database in Cloud Spanner.

        :type project_id: str
        :param instance_id: The ID of the Cloud Spanner instance.
        :type instance_id: str
        :param database_id: The ID of the database to create in Cloud Spanner.
        :type database_id: str
        :param ddl_statements: The string list containing DDL for the new database.
        :type ddl_statements: list[str]
        :param project_id: Optional, the ID of the  GCP project that owns the Cloud Spanner
            database. If set to None or missing, the default project_id from the GCP connection is used.
        :return: None
        """
    instance = self._get_client(project_id=project_id).instance(instance_id=instance_id)
    if not instance.exists():
        raise AirflowException('The instance {} does not exist in project {} !'.format(instance_id, project_id))
    database = instance.database(database_id=database_id, ddl_statements=ddl_statements)
    try:
        operation = database.create()
    except GoogleAPICallError as e:
        self.log.error('An error occurred: %s. Exiting.', e.message)
        raise e
    if operation:
        result = operation.result()
        self.log.info(result)
    return