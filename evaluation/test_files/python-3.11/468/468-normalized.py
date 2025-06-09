def delete_file(self, container_name, blob_name, is_prefix=False, ignore_if_missing=False, **kwargs):
    """
        Delete a file from Azure Blob Storage.

        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param is_prefix: If blob_name is a prefix, delete all matching files
        :type is_prefix: bool
        :param ignore_if_missing: if True, then return success even if the
            blob does not exist.
        :type ignore_if_missing: bool
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.create_blob_from_path()` takes.
        :type kwargs: object
        """
    if is_prefix:
        blobs_to_delete = [blob.name for blob in self.connection.list_blobs(container_name, prefix=blob_name, **kwargs)]
    elif self.check_for_blob(container_name, blob_name):
        blobs_to_delete = [blob_name]
    else:
        blobs_to_delete = []
    if not ignore_if_missing and len(blobs_to_delete) == 0:
        raise AirflowException('Blob(s) not found: {}'.format(blob_name))
    for blob_uri in blobs_to_delete:
        self.log.info('Deleting blob: ' + blob_uri)
        self.connection.delete_blob(container_name, blob_uri, delete_snapshots='include', **kwargs)