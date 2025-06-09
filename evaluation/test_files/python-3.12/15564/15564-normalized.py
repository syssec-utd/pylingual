def list(self, path):
    """List the entities found directly under the given path.

        Args:
            path (str): The path of the entity to be listed. Must start with a '/'.

        Returns:
            The list of entity names directly under the given path:

                u'/12345/folder_1'

        Raises:
            StorageArgumentException: Invalid arguments
            StorageForbiddenException: Server response code 403
            StorageNotFoundException: Server response code 404
            StorageException: other 400-600 error codes
        """
    self.__validate_storage_path(path)
    entity = self.api_client.get_entity_by_query(path=path)
    if entity['entity_type'] not in self.__BROWSABLE_TYPES:
        raise StorageArgumentException('The entity type "{0}" cannot belisted'.format(entity['entity_type']))
    entity_uuid = entity['uuid']
    file_names = []
    more_pages = True
    page_number = 1
    while more_pages:
        response = self.api_client.list_folder_content(entity_uuid, page=page_number, ordering='name')
        more_pages = response['next'] is not None
        page_number += 1
        for child in response['results']:
            pattern = '/{name}' if child['entity_type'] == 'folder' else '{name}'
            file_names.append(pattern.format(name=child['name']))
    return file_names