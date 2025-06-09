def _message_symbol(self, msgid):
    """Get the message symbol of the given message id

        Return the original message id if the message does not
        exist.
        """
    try:
        return [md.symbol for md in self.msgs_store.get_message_definitions(msgid)]
    except UnknownMessageError:
        return msgid