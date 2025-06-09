def get_query_includes(tokenized_terms, search_fields):
    """
    Builds a query for included terms in a text search.
    """
    query = None
    for term in tokenized_terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{'%s__icontains' % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query