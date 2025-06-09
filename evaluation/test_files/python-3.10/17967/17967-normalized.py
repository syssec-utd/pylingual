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
    return self.resources.get_token(token_name, project_name, dataset_name)