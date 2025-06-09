def match(self, table, nomatch=0):
    """
        Make a vector of the positions of (first) matches of its first argument in its second.

        Only applicable to single-column categorical/string frames.

        :param List table: the list of items to match against
        :param int nomatch: value that should be returned when there is no match.
        :returns: a new H2OFrame containing for each cell from the source frame the index where
            the pattern ``table`` first occurs within that cell.
        """
    return H2OFrame._expr(expr=ExprNode('match', self, table, nomatch, None))