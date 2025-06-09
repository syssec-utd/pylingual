def drop_matching_records(self, check):
    """Remove a record from the DB."""
    expr, args = self._render_expression(check)
    query = 'DELETE FROM %s WHERE %s' % (self.table, expr)
    self._db.execute(query, args)