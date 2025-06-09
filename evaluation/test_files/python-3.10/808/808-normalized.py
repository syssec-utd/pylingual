def get_conn(self):
    """
        Establishes a connection depending on the security mode set via config or environment variable.

        :return: a hdfscli InsecureClient or KerberosClient object.
        :rtype: hdfs.InsecureClient or hdfs.ext.kerberos.KerberosClient
        """
    connections = self.get_connections(self.webhdfs_conn_id)
    for connection in connections:
        try:
            self.log.debug('Trying namenode %s', connection.host)
            client = self._get_client(connection)
            client.status('/')
            self.log.debug('Using namenode %s for hook', connection.host)
            return client
        except HdfsError as hdfs_error:
            self.log.debug('Read operation on namenode %s failed with error: %s', connection.host, hdfs_error)
    hosts = [connection.host for connection in connections]
    error_message = 'Read operations failed on the namenodes below:\n{hosts}'.format(hosts='\n'.join(hosts))
    raise AirflowWebHDFSHookException(error_message)