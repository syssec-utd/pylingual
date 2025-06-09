def does_collection_exist(self, collection_name, database_name=None):
    """
        Checks if a collection exists in CosmosDB.
        """
    if collection_name is None:
        raise AirflowBadRequest('Collection name cannot be None.')
    existing_container = list(self.get_conn().QueryContainers(get_database_link(self.__get_database_name(database_name)), {'query': 'SELECT * FROM r WHERE r.id=@id', 'parameters': [{'name': '@id', 'value': collection_name}]}))
    if len(existing_container) == 0:
        return False
    return True