def get_items(self, url, params=None, **kwargs):
    """Return a generator that GETs and yields individual JSON `items`.

        Yields individual `items` from Webex Teams's top-level {'items': [...]}
        JSON objects. Provides native support for RFC5988 Web Linking.  The
        generator will request additional pages as needed until all items have
        been returned.

        Args:
            url(basestring): The URL of the API endpoint.
            params(dict): The parameters for the HTTP GET request.
            **kwargs:
                erc(int): The expected (success) response code for the request.
                others: Passed on to the requests package.

        Raises:
            ApiError: If anything other than the expected response code is
                returned by the Webex Teams API endpoint.
            MalformedResponse: If the returned response does not contain a
                top-level dictionary with an 'items' key.

        """
    pages = self.get_pages(url, params=params, **kwargs)
    for json_page in pages:
        assert isinstance(json_page, dict)
        items = json_page.get('items')
        if items is None:
            error_message = "'items' key not found in JSON data: {!r}".format(json_page)
            raise MalformedResponse(error_message)
        else:
            for item in items:
                yield item