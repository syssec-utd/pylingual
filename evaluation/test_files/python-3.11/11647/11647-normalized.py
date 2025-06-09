def nr_cases(self, institute_id=None):
    """Return the number of cases

        This function will change when we migrate to 3.7.1

        Args:
            collaborator(str): Institute id

        Returns:
            nr_cases(int)
        """
    query = {}
    if institute_id:
        query['collaborators'] = institute_id
    LOG.debug('Fetch all cases with query {0}'.format(query))
    nr_cases = self.case_collection.find(query).count()
    return nr_cases