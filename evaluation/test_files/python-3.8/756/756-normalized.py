def table_exists(self, table):
    """
        Checks if a table exists in Cassandra

        :param table: Target Cassandra table.
                      Use dot notation to target a specific keyspace.
        :type table: str
        """
    keyspace = self.keyspace
    if '.' in table:
        (keyspace, table) = table.split('.', 1)
    cluster_metadata = self.get_conn().cluster.metadata
    return keyspace in cluster_metadata.keyspaces and table in cluster_metadata.keyspaces[keyspace].tables