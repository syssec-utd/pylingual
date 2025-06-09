def search(self, query=None, args=None):
    """query will show images determined by the extension of img
       or simg.

       Parameters
       ==========
       query: the container name (path) or uri to search for
       args.endpoint: can be an endpoint id and optional path, e.g.:

             --endpoint  6881ae2e-db26-11e5-9772-22000b9da45e:.singularity'
             --endpoint  6881ae2e-db26-11e5-9772-22000b9da45e'

       if not defined, we show the user endpoints to choose from

       Usage
       =====
       If endpoint is defined with a query, then we search the given endpoint
       for a container of interested (designated by ending in .img or .simg

       If no endpoint is provided but instead just a query, we use the query
       to search endpoints.
    
    """
    if query is None:
        if args.endpoint is None:
            bot.info('Listing shared endpoints. Add query to expand search.')
            return self._list_endpoints()
        else:
            return self._list_endpoint(args.endpoint)
    if args.endpoint is None:
        bot.info('You must specify an endpoint id to query!')
        return self._list_endpoints(query)
    return self._list_endpoint(endpoint=args.endpoint, query=query)