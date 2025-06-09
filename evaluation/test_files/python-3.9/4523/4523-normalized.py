def close(self):
    """
        Call close() for all plugins
        """
    logger.info('Close allocated resources...')
    for plugin in self.plugins.values():
        logger.debug('Close %s', plugin)
        try:
            plugin.close()
        except Exception as ex:
            logger.error('Failed closing plugin %s: %s', plugin, ex)
            logger.debug('Failed closing plugin: %s', traceback.format_exc(ex))