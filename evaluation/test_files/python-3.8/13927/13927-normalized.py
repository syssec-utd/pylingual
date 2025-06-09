def expression_filters(self):
    """ Dict[str, ExpressionFilter]: Returns the expression filters for this selector. """
    return {name: filter for (name, filter) in iter(self.filters.items()) if isinstance(filter, ExpressionFilter)}