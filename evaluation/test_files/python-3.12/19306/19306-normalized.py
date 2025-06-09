def line_received(self, line):
    """
        Called when a complete line is found from the remote worker. Decodes
        a response object from the line, then passes it to the worker object.
        """
    response = json.loads(line.decode('utf-8'))
    self._worker.response_received(response)