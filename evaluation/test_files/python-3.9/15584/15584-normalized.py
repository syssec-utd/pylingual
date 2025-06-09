def delete_metadata(self, entity_type, entity_id, metadata_keys):
    """Delete the selected metadata entries of an entity.

        Only deletes selected metadata keys, for a complete wipe, use set_metadata.

        Args:
            entity_type (str): Type of the entity. Admitted values: ['project',
                'folder', 'file'].
            entity_id (srt): The UUID of the entity to be modified.
            metadata_keys (lst): A list of metada keys to be deleted.

        Returns:
            A dictionary of the updated object metadata::

                {
                    u'bar': u'200',
                    u'foo': u'100'
                }

        Raises:
            StorageArgumentException: Invalid arguments
            StorageForbiddenException: Server response code 403
            StorageNotFoundException: Server response code 404
            StorageException: other 400-600 error codes
        """
    if not is_valid_uuid(entity_id):
        raise StorageArgumentException('Invalid UUID for entity_id: {0}'.format(entity_id))
    if not isinstance(metadata_keys, list):
        raise StorageArgumentException('The metadata was not provided as a dictionary')
    return self._authenticated_request.to_endpoint('{}/{}/metadata/'.format(entity_type, entity_id)).with_json_body({'keys': metadata_keys}).return_body().delete()