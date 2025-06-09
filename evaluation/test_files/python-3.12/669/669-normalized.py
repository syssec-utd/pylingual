def restore_from_cluster_snapshot(self, cluster_identifier, snapshot_identifier):
    """
        Restores a cluster from its snapshot

        :param cluster_identifier: unique identifier of a cluster
        :type cluster_identifier: str
        :param snapshot_identifier: unique identifier for a snapshot of a cluster
        :type snapshot_identifier: str
        """
    response = self.get_conn().restore_from_cluster_snapshot(ClusterIdentifier=cluster_identifier, SnapshotIdentifier=snapshot_identifier)
    return response['Cluster'] if response['Cluster'] else None