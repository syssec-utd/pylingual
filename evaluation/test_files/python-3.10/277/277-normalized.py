def get_model(self, project_id, model_name):
    """
        Gets a Model. Blocks until finished.
        """
    if not model_name:
        raise ValueError('Model name must be provided and it could not be an empty string')
    full_model_name = 'projects/{}/models/{}'.format(project_id, model_name)
    request = self._mlengine.projects().models().get(name=full_model_name)
    try:
        return request.execute()
    except HttpError as e:
        if e.resp.status == 404:
            self.log.error('Model was not found: %s', e)
            return None
        raise