def fetch_items(self, category, **kwargs):
    """Fetch items

        :param category: the category of items to fetch
        :param kwargs: backend arguments

        :returns: a generator of items
        """
    offset = kwargs['offset']
    logger.info("Looking for events at url '%s' of %s category and %i offset", self.url, category, offset)
    nitems = 0
    titems = 0
    page = int(offset / ReMoClient.ITEMS_PER_PAGE)
    page_offset = page * ReMoClient.ITEMS_PER_PAGE
    drop_items = offset - page_offset
    logger.debug('%i items dropped to get %i offset starting in page %i (%i page offset)', drop_items, offset, page, page_offset)
    current_offset = offset
    for raw_items in self.client.get_items(category, offset):
        items_data = json.loads(raw_items)
        titems = items_data['count']
        logger.info('Pending items to retrieve: %i, %i current offset', titems - current_offset, current_offset)
        items = items_data['results']
        for item in items:
            if drop_items > 0:
                drop_items -= 1
                continue
            raw_item_details = self.client.fetch(item['_url'])
            item_details = json.loads(raw_item_details)
            item_details['offset'] = current_offset
            current_offset += 1
            yield item_details
            nitems += 1
    logger.info('Total number of events: %i (%i total, %i offset)', nitems, titems, offset)