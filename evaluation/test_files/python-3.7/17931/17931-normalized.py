def get_token(self, token_name, project_name, dataset_name):
    """
        Get a token with the given parameters.
        Arguments:
            project_name (str): Project name
            dataset_name (str): Dataset name project is based on
            token_name (str): Token name
        Returns:
            dict: Token info
        """
    url = self.url() + '/nd/resource/dataset/{}'.format(dataset_name) + '/project/{}'.format(project_name) + '/token/{}/'.format(token_name)
    req = self.remote_utils.get_url(url)
    if req.status_code is not 200:
        raise RemoteDataUploadError('Could not find {}'.format(req.text))
    else:
        return req.json()