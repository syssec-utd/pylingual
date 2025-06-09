def search(self, name, query_fields=None):
    """Searches the OLS with the given term

        :param str name:
        :param list[str] query_fields: Fields to query
        :return: dict
        """
    params = {'q': name}
    if query_fields is not None:
        params['queryFields'] = '{{{}}}'.format(','.join(query_fields))
    response = requests.get(self.ontology_search, params=params)
    return response.json()