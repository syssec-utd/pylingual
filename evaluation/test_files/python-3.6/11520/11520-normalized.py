def indexes(self, collection=None):
    """Return a list with the current indexes
        
        Skip the mandatory _id_ indexes
        
        Args:
            collection(str)

        Returns:
            indexes(list)
        """
    indexes = []
    for collection_name in self.collections():
        if collection and collection != collection_name:
            continue
        for index_name in self.db[collection_name].index_information():
            if index_name != '_id_':
                indexes.append(index_name)
    return indexes