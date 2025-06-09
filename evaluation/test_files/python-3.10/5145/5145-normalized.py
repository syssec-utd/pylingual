def fetch_items(self, category, **kwargs):
    """Fetch the messages

        :param category: the category of items to fetch
        :param kwargs: backend arguments

        :returns: a generator of items
        """
    offset = kwargs['offset']
    chats = kwargs['chats']
    logger.info("Looking for messages of '%s' bot from offset '%s'", self.bot, offset)
    if chats is not None:
        if len(chats) == 0:
            logger.warning('Chat list filter is empty. No messages will be returned')
        else:
            logger.info('Messages which belong to chats %s will be fetched', '[' + ','.join((str(ch_id) for ch_id in chats)) + ']')
    nmsgs = 0
    while True:
        raw_json = self.client.updates(offset=offset)
        messages = [msg for msg in self.parse_messages(raw_json)]
        if len(messages) == 0:
            break
        for msg in messages:
            offset = max(msg['update_id'], offset)
            if not self._filter_message_by_chats(msg, chats):
                logger.debug('Message %s does not belong to any chat; filtered', msg['message']['message_id'])
                continue
            yield msg
            nmsgs += 1
        offset += 1
    logger.info('Fetch process completed: %s messages fetched', nmsgs)