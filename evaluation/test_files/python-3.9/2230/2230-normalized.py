def _log_start_transaction(self, endpoint, data, json, files, params):
    """Log the beginning of an API request."""
    self._requests_counter += 1
    if not self._is_logging:
        return
    msg = '\n---- %d --------------------------------------------------------\n' % self._requests_counter
    msg += '[%s] %s\n' % (time.strftime('%H:%M:%S'), endpoint)
    if params is not None:
        msg += '     params: {%s}\n' % ', '.join(('%s:%s' % item for item in viewitems(params)))
    if data is not None:
        msg += '     body: {%s}\n' % ', '.join(('%s:%s' % item for item in viewitems(data)))
    if json is not None:
        import json as j
        msg += '     json: %s\n' % j.dumps(json)
    if files is not None:
        msg += '     file: %s\n' % ', '.join((f.name for f in viewvalues(files)))
    self._log_message(msg + '\n')