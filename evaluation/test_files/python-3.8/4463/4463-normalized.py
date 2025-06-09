def _collect_data(self, end=False):
    """
        Collect data, cache it and send to listeners
        """
    data = get_nowait_from_queue(self.results)
    stats = get_nowait_from_queue(self.stats_results)
    logger.debug('Data timestamps: %s' % [d.get('ts') for d in data])
    logger.debug('Stats timestamps: %s' % [d.get('ts') for d in stats])
    for item in data:
        ts = item['ts']
        if ts in self.stat_cache:
            data_item = item
            stat_item = self.stat_cache.pop(ts)
            self.__notify_listeners(data_item, stat_item)
        else:
            self.data_cache[ts] = item
    for item in stats:
        ts = item['ts']
        if ts in self.data_cache:
            data_item = self.data_cache.pop(ts)
            stat_item = item
            self.__notify_listeners(data_item, stat_item)
        else:
            self.stat_cache[ts] = item
    if end and len(self.data_cache) > 0:
        logger.info('Timestamps without stats:')
        for (ts, data_item) in sorted(self.data_cache.items(), key=lambda i: i[0]):
            logger.info(ts)
            self.__notify_listeners(data_item, StatsReader.stats_item(ts, 0, 0))