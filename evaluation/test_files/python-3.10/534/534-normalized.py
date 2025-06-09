def delete_instance(self, instance_id, project_id=None):
    """
        Deletes the specified Cloud Bigtable instance.
        Raises google.api_core.exceptions.NotFound if the Cloud Bigtable instance does
        not exist.

        :param project_id: Optional, Google Cloud Platform project ID where the
            BigTable exists. If set to None or missing,
            the default project_id from the GCP connection is used.
        :type project_id: str
        :param instance_id: The ID of the Cloud Bigtable instance.
        :type instance_id: str
        """
    instance = self.get_instance(instance_id=instance_id, project_id=project_id)
    if instance:
        instance.delete()
    else:
        self.log.info("The instance '%s' does not exist in project '%s'. Exiting", instance_id, project_id)