def delete_file(self, file_id):
    """Delete a file.

        Args:
            file_id (str): The UUID of the file to delete.

        Returns:
            None

        Raises:
            StorageArgumentException: Invalid arguments
            StorageForbiddenException: Server response code 403
            StorageNotFoundException: Server response code 404
            StorageException: other 400-600 error codes
        """
    if not is_valid_uuid(file_id):
        raise StorageArgumentException('Invalid UUID for file_id: {0}'.format(file_id))
    self._authenticated_request.to_endpoint('file/{}/'.format(file_id)).delete()