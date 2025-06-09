def new(cls, access_token, environment='prod'):
    """Creates a new cross-service client."""
    return cls(storage_client=StorageClient.new(access_token, environment=environment))