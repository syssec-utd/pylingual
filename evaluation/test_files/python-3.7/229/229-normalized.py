def lookup(self, keys, read_consistency=None, transaction=None):
    """
        Lookup some entities by key.

        .. seealso::
            https://cloud.google.com/datastore/docs/reference/rest/v1/projects/lookup

        :param keys: the keys to lookup.
        :type keys: list
        :param read_consistency: the read consistency to use. default, strong or eventual.
                                 Cannot be used with a transaction.
        :type read_consistency: str
        :param transaction: the transaction to use, if any.
        :type transaction: str
        :return: the response body of the lookup request.
        :rtype: dict
        """
    conn = self.get_conn()
    body = {'keys': keys}
    if read_consistency:
        body['readConsistency'] = read_consistency
    if transaction:
        body['transaction'] = transaction
    resp = conn.projects().lookup(projectId=self.project_id, body=body).execute(num_retries=self.num_retries)
    return resp