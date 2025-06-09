def _apply_to_instance(self, project_id, instance_id, configuration_name, node_count, display_name, func):
    """
        Invokes a method on a given instance by applying a specified Callable.

        :param project_id: The ID of the  GCP project that owns the Cloud Spanner
            database.
        :type project_id: str
        :param instance_id: The ID of the instance.
        :type instance_id: str
        :param configuration_name: Name of the instance configuration defining how the
            instance will be created. Required for instances which do not yet exist.
        :type configuration_name: str
        :param node_count: (Optional) Number of nodes allocated to the instance.
        :type node_count: int
        :param display_name: (Optional) The display name for the instance in the Cloud
            Console UI. (Must be between 4 and 30 characters.) If this value is not set
            in the constructor, will fall back to the instance ID.
        :type display_name: str
        :param func: Method of the instance to be called.
        :type func: Callable
        """
    instance = self._get_client(project_id=project_id).instance(instance_id=instance_id, configuration_name=configuration_name, node_count=node_count, display_name=display_name)
    try:
        operation = func(instance)
    except GoogleAPICallError as e:
        self.log.error('An error occurred: %s. Exiting.', e.message)
        raise e
    if operation:
        result = operation.result()
        self.log.info(result)