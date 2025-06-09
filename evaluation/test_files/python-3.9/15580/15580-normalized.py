def get_entity_by_query(self, uuid=None, path=None, metadata=None):
    """Retrieve entity by query param which can be either uuid/path/metadata.

        Args:
            uuid (str): The UUID of the requested entity.
            path (str): The path of the requested entity.
            metadata (dict): A dictionary of one metadata {key: value} of the
                requested entitity.

        Returns:
            The details of the entity, if found::

                {
                    u'content_type': u'plain/text',
                    u'created_by': u'303447',
                    u'created_on': u'2017-03-13T10:52:23.275087Z',
                    u'description': u'',
                    u'entity_type': u'file',
                    u'modified_by': u'303447',
                    u'modified_on': u'2017-03-13T10:52:23.275126Z',
                    u'name': u'myfile',
                    u'parent': u'3abd8742-d069-44cf-a66b-2370df74a682',
                    u'uuid': u'e2c25c1b-f6a9-4cf6-b8d2-271e628a9a56'
                }

        Raises:
            StorageArgumentException: Invalid arguments
            StorageForbiddenException: Server response code 403
            StorageNotFoundException: Server response code 404
            StorageException: other 400-600 error codes
        """
    if not (uuid or path or metadata):
        raise StorageArgumentException('No parameter given for the query.')
    if uuid and (not is_valid_uuid(uuid)):
        raise StorageArgumentException('Invalid UUID for uuid: {0}'.format(uuid))
    params = locals().copy()
    if metadata:
        if not isinstance(metadata, dict):
            raise StorageArgumentException('The metadata needs to be provided as a dictionary.')
        (key, value) = next(iter(metadata.items()))
        params[key] = value
        del params['metadata']
    params = self._prep_params(params)
    return self._authenticated_request.to_endpoint('entity/').with_params(params).return_body().get()