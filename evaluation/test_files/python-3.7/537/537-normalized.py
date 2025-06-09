def delete_table(self, instance_id, table_id, project_id=None):
    """
        Deletes the specified table in Cloud Bigtable.
        Raises google.api_core.exceptions.NotFound if the table does not exist.

        :type instance_id: str
        :param instance_id: The ID of the Cloud Bigtable instance.
        :type table_id: str
        :param table_id: The ID of the table in Cloud Bigtable.
        :type project_id: str
        :param project_id: Optional, Google Cloud Platform project ID where the
            BigTable exists. If set to None or missing,
            the default project_id from the GCP connection is used.
        """
    table = self.get_instance(instance_id=instance_id, project_id=project_id).table(table_id=table_id)
    table.delete()