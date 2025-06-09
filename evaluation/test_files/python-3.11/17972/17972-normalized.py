def delete_channel(self, channel_name, project_name, dataset_name):
    """
        Deletes a channel given its name, name of its project
        , and name of its dataset.

        Arguments:
            channel_name (str): Channel name
            project_name (str): Project name
            dataset_name (str): Dataset name

        Returns:
            bool: True if channel deleted, False if not
        """
    return self.resources.delete_channel(channel_name, project_name, dataset_name)