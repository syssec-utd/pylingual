def track_trace(self, name: str, properties: Dict[str, object]=None, severity=None):
    """
        Sends a single trace statement.
        :param name: the trace statement.

        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)

        :param severity: the severity level of this trace, one of DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
    self._client.track_trace(name, properties, severity)