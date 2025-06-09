def Or(cls, *requirements):
    """
        Short cut helper to construct a combinator that uses
        :meth:`operator.or_` to reduce requirement results and stops evaluating
        on the first True.

        This is also exported at the module level as ``Or``
        """
    return cls(*requirements, op=operator.or_, until=True)