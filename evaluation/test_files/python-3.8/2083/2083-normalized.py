def group_by(self, by):
    """
        Return a new ``GroupBy`` object using this frame and the desired grouping columns.

        The returned groups are sorted by the natural group-by column sort.

        :param by: The columns to group on (either a single column name, or a list of column names, or
            a list of column indices).
        """
    assert_is_type(by, str, int, [str, int])
    return GroupBy(self, by)