def get_object_from_salesforce(self, obj, fields):
    """
        Get all instances of the `object` from Salesforce.
        For each model, only get the fields specified in fields.

        All we really do underneath the hood is run:
            SELECT <fields> FROM <obj>;

        :param obj: The object name to get from Salesforce.
        :type obj: str
        :param fields: The fields to get from the object.
        :type fields: iterable
        :return: all instances of the object from Salesforce.
        :rtype: dict
        """
    query = 'SELECT {} FROM {}'.format(','.join(fields), obj)
    self.log.info('Making query to Salesforce: %s', query if len(query) < 30 else ' ... '.join([query[:15], query[-15:]]))
    return self.make_query(query)