def container_query(self, query):
    """search for a specific container.
    This function would likely be similar to the above, but have different
    filter criteria from the user (based on the query)
    """
    results = set()
    query = remove_uri(query)
    for container in self.conn.get_account()[1]:
        for result in self.conn.get_container(container['name'])[1]:
            if query in collection['name']:
                results.add('%s/%s' % (container['name'], result['name']))
    if len(results) == 0:
        bot.info('No container collections found.')
        sys.exit(1)
    bot.info('Collections')
    bot.table([list(results)])
    return list(results)