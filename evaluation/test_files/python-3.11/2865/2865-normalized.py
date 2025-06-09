def get_job(self, cloud_service_id, job_collection_id, job_id):
    """
        The Get Job operation gets the details (including the current job status)
        of the specified job from the specified job collection.

        The return type is

        cloud_service_id:
            The cloud service id
        job_collection_id:
            Name of the hosted service.
        job_id:
            The job id you wish to create.
        """
    _validate_not_none('cloud_service_id', cloud_service_id)
    _validate_not_none('job_collection_id', job_collection_id)
    _validate_not_none('job_id', job_id)
    path = self._get_job_collection_path(cloud_service_id, job_collection_id, job_id)
    self.content_type = 'application/json'
    payload = self._perform_get(path).body.decode()
    return json.loads(payload)