def _build_extra_predicate(self, extra_predicate):
    """ This method is a good one to extend if you want to create a queue which always applies an extra predicate. """
    if extra_predicate is None:
        return ''
    if not isinstance(extra_predicate[1], (list, dict, tuple)):
        extra_predicate = [extra_predicate[0], (extra_predicate[1],)]
    extra_predicate = database.escape_query(*extra_predicate)
    return 'AND (' + extra_predicate + ')'