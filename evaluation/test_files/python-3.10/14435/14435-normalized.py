def get_mapping(self, index=None, doc_type=None, params=None):
    """
        Retrieve mapping definition of index or index/type.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-mapping.html>`_
        :arg index: A comma-separated list of index names
        :arg doc_type: A comma-separated list of document types
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
    (_, data) = (yield self.transport.perform_request('GET', _make_path(index, '_mapping', doc_type), params=params))
    raise gen.Return(data)