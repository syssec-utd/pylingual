def fetch_items(self, category, **kwargs):
    """Fetch the events

        :param category: the category of items to fetch
        :param kwargs: backend arguments

        :returns: a generator of items
        """
    from_date = kwargs['from_date']
    to_date = kwargs['to_date']
    logger.info("Fetching events of '%s' group from %s to %s", self.group, str(from_date), str(to_date) if to_date else '--')
    to_date_ts = datetime_to_utc(to_date).timestamp() if to_date else None
    nevents = 0
    stop_fetching = False
    ev_pages = self.client.events(self.group, from_date=from_date)
    for evp in ev_pages:
        events = [event for event in self.parse_json(evp)]
        for event in events:
            event_id = event['id']
            event['comments'] = self.__fetch_and_parse_comments(event_id)
            event['rsvps'] = self.__fetch_and_parse_rsvps(event_id)
            event_ts = self.metadata_updated_on(event)
            if to_date_ts and event_ts >= to_date_ts:
                stop_fetching = True
                continue
            yield event
            nevents += 1
        if stop_fetching:
            break
    logger.info('Fetch process completed: %s events fetched', nevents)