def get_conn(self):
    """
        Return a cosmos db client.
        """
    if self.cosmos_client is not None:
        return self.cosmos_client
    self.cosmos_client = cosmos_client.CosmosClient(self.endpoint_uri, {'masterKey': self.master_key})
    return self.cosmos_client