def get_dataset(self, name):
    """
        Returns info regarding a particular dataset.

        Arugments:
            name (str): Dataset name

        Returns:
            dict: Dataset information
        """
    url = self.url() + '/resource/dataset/{}'.format(name)
    req = self.remote_utils.get_url(url)
    if req.status_code is not 200:
        raise RemoteDataNotFoundError('Could not find {}'.format(req.text))
    else:
        return req.json()