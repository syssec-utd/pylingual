def get_results(self, hql, schema='default', fetch_size=None, hive_conf=None):
    """
        Get results of the provided hql in target schema.

        :param hql: hql to be executed.
        :type hql: str or list
        :param schema: target schema, default to 'default'.
        :type schema: str
        :param fetch_size: max size of result to fetch.
        :type fetch_size: int
        :param hive_conf: hive_conf to execute alone with the hql.
        :type hive_conf: dict
        :return: results of hql execution, dict with data (list of results) and header
        :rtype: dict
        """
    results_iter = self._get_results(hql, schema, fetch_size=fetch_size, hive_conf=hive_conf)
    header = next(results_iter)
    results = {'data': list(results_iter), 'header': header}
    return results