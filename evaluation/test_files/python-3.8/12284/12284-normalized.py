def get_container(self, container, headers=None, prefix=None, delimiter=None, marker=None, end_marker=None, limit=None, query=None, cdn=False, decode_json=True):
    """
        GETs the container and returns the results. This is done to
        list the objects for the container. Some useful headers are
        also returned:

        =========================== =================================
        x-container-bytes-used      Object storage used for the
                                    container, in bytes.
        x-container-object-count    The number of objects in the
                                    container.
        =========================== =================================

        Also, any user headers beginning with x-container-meta- are
        returned.

        These values can be delayed depending the Swift cluster.

        :param container: The name of the container.
        :param headers: Additional headers to send with the request.
        :param prefix: The prefix object names must match to be
            listed.
        :param delimiter: The delimiter for the listing. Delimiters
            indicate how far to progress through object names before
            "rolling them up". For instance, a delimiter='/' query on
            an container with the objects::

                one/one
                one/two
                two
                three/one

            would return the JSON value of::

                [{'subdir': 'one/'},
                 {'count': 0, 'bytes': 0, 'name': 'two'},
                 {'subdir': 'three/'}]

            Using this with prefix can allow you to traverse a psuedo
            hierarchy.
        :param marker: Only object names after this marker will be
            returned. Swift returns a limited number of objects per
            request (often 10,000). To get the next batch of names,
            you issue another query with the marker set to the last
            name you received. You can continue to issue requests
            until you receive no more names.
        :param end_marker: Only object names before this marker will be
            returned.
        :param limit: Limits the size of the list returned per
            request. The default and maximum depends on the Swift
            cluster (usually 10,000).
        :param query: Set to a dict of query values to send on the
            query string of the request.
        :param cdn: If set True, the CDN management interface will be
            used.
        :param decode_json: If set False, the usual decoding of the
            JSON response will be skipped and the raw contents will
            be returned instead.
        :returns: A tuple of (status, reason, headers, contents).

            :status: is an int for the HTTP status code.
            :reason: is the str for the HTTP status (ex: "Ok").
            :headers: is a dict with all lowercase keys of the HTTP
                headers; if a header has multiple values, it will be a
                list.
            :contents: is the decoded JSON response or the raw str
                for the HTTP body.
        """
    query = dict(query or {})
    query['format'] = 'json'
    if prefix:
        query['prefix'] = prefix
    if delimiter:
        query['delimiter'] = delimiter
    if marker:
        query['marker'] = marker
    if end_marker:
        query['end_marker'] = end_marker
    if limit:
        query['limit'] = limit
    return self.request('GET', self._container_path(container), '', headers, decode_json=decode_json, query=query, cdn=cdn)