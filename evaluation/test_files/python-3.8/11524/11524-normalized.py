def build_variant_query(self, query=None, category='snv', variant_type=['clinical']):
    """Build a mongo query across multiple cases.
        Translate query options from a form into a complete mongo query dictionary.

        Beware that unindexed queries against a large variant collection will
        be extremely slow.

        Currently indexed query options:
            hgnc_symbols
            rank_score
            variant_type
            category

        Args:
            query(dict): A query dictionary for the database, from a query form.
            category(str): 'snv', 'sv', 'str' or 'cancer'
            variant_type(str): 'clinical' or 'research'

        Returns:
            mongo_query : A dictionary in the mongo query format.
        """
    query = query or {}
    mongo_variant_query = {}
    LOG.debug('Building a mongo query for %s' % query)
    if query.get('hgnc_symbols'):
        mongo_variant_query['hgnc_symbols'] = {'$in': query['hgnc_symbols']}
    mongo_variant_query['variant_type'] = {'$in': variant_type}
    mongo_variant_query['category'] = category
    rank_score = query.get('rank_score') or 15
    mongo_variant_query['rank_score'] = {'$gte': rank_score}
    LOG.debug('Querying %s' % mongo_variant_query)
    return mongo_variant_query