def get_data(self, cache=True, as_text=False, parse_form_data=False):
    """This reads the buffered incoming data from the client into one
        bytestring.  By default this is cached but that behavior can be
        changed by setting `cache` to `False`.

        Usually it's a bad idea to call this method without checking the
        content length first as a client could send dozens of megabytes or more
        to cause memory problems on the server.

        Note that if the form data was already parsed this method will not
        return anything as form data parsing does not cache the data like
        this method does.  To implicitly invoke form data parsing function
        set `parse_form_data` to `True`.  When this is done the return value
        of this method will be an empty string if the form parser handles
        the data.  This generally is not necessary as if the whole data is
        cached (which is the default) the form parser will used the cached
        data to parse the form data.  Please be generally aware of checking
        the content length first in any case before calling this method
        to avoid exhausting server memory.

        If `as_text` is set to `True` the return value will be a decoded
        unicode string.

        .. versionadded:: 0.9
        """
    rv = getattr(self, '_cached_data', None)
    if rv is None:
        if parse_form_data:
            self._load_form_data()
        rv = self.stream.read()
        if cache:
            self._cached_data = rv
    if as_text:
        rv = rv.decode(self.charset, self.encoding_errors)
    return rv