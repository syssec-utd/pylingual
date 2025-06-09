def resolve_expression(self, *args, **kwargs) -> HStoreColumn:
    """Resolves the expression into a :see:HStoreColumn expression."""
    original_expression = super().resolve_expression(*args, **kwargs)
    expression = HStoreColumn(original_expression.alias, original_expression.target, self.key)
    return expression