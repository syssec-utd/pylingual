def apply_filter(self, expr, value):
    """
        Returns the given expression filtered by the given value.

        Args:
            expr (xpath.expression.AbstractExpression): The expression to filter.
            value (object): The desired value with which the expression should be filtered.

        Returns:
            xpath.expression.AbstractExpression: The filtered expression.
        """
    if self.skip(value):
        return expr
    if not self._valid_value(value):
        msg = 'Invalid value {value} passed to filter {name} - '.format(value=repr(value), name=self.name)
        if self.default is not None:
            warn(msg + 'defaulting to {}'.format(self.default))
            value = self.default
        else:
            warn(msg + 'skipping')
            return expr
    return self.func(expr, value)