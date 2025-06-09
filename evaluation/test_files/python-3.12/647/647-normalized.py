def _build_opsgenie_payload(self):
    """
        Construct the Opsgenie JSON payload. All relevant parameters are combined here
        to a valid Opsgenie JSON payload.

        :return: Opsgenie payload (dict) to send
        """
    payload = {}
    for key in ['message', 'alias', 'description', 'responders', 'visibleTo', 'actions', 'tags', 'details', 'entity', 'source', 'priority', 'user', 'note']:
        val = getattr(self, key)
        if val:
            payload[key] = val
    return payload