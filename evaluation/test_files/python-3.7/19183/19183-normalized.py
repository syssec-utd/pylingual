def not_in(self, table):
    """
        Select nuclei not in table

        Parameters
        ----------
        table: Table, Table object from where nuclei should be removed

        Example:
        ----------
        Find the new nuclei in AME2003 with Z,N >= 8:

        >>> Table('AME2003').not_in(Table('AME1995'))[8:,8:].count
        389
        """
    idx = self.df.index - table.df.index
    return Table(df=self.df[idx], name=self.name)