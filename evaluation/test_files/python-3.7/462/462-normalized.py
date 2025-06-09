def check_for_blob(self, container_name, blob_name, **kwargs):
    """
        Check if a blob exists on Azure Blob Storage.

        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.exists()` takes.
        :type kwargs: object
        :return: True if the blob exists, False otherwise.
        :rtype: bool
        """
    return self.connection.exists(container_name, blob_name, **kwargs)