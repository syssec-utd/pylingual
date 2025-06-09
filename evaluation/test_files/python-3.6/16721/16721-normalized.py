def lock_connection(cls, conf, dsn, key=None):
    """
        A class method to lock a connection (given by :code:`dsn`) in the specified
        configuration file. Automatically opens the file and writes to it before
        closing.

        :param str conf: The configuration file to modify
        :param str dsn: The name of the connection to lock
        :raises `giraffez.errors.ConfigurationError`: if the connection does not exist
        """
    with Config(conf, 'w', key) as c:
        connection = c.get_connection(dsn)
        if not connection:
            raise ConfigurationError('Unable to lock connection')
        if dsn is None:
            dsn = c.settings['connections']['default']
        value = 'connections.{}.lock'.format(dsn)
        lock = c.get_value('connections.{}.lock'.format(dsn), default=0)
        if lock >= 2:
            raise ConnectionLock(dsn)
        lock += 1
        c.set_value('connections.{}.lock'.format(dsn), lock)
        c.write()