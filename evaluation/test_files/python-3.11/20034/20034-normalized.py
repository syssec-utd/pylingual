def purge_queue(self, name):
    """Create message content and properties to purge queue with QMFv2

        :param name: Name of queue to purge
        :type name: str

        :returns: Tuple containing content and method properties
        """
    content = {'_object_id': {'_object_name': 'org.apache.qpid.broker:queue:{0}'.format(name)}, '_method_name': 'purge', '_arguments': {'type': 'queue', 'name': name, 'filter': dict()}}
    logger.debug('Message content -> {0}'.format(content))
    return (content, self.method_properties)