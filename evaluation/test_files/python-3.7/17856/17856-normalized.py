def any_decimal_field(field, **kwargs):
    """
    Return random value for DecimalField

    >>> result = any_field(models.DecimalField(max_digits=5, decimal_places=2))
    >>> type(result)
    <class 'decimal.Decimal'>
    """
    min_value = kwargs.get('min_value', 0)
    max_value = kwargs.get('max_value', Decimal('%s.%s' % ('9' * (field.max_digits - field.decimal_places), '9' * field.decimal_places)))
    decimal_places = kwargs.get('decimal_places', field.decimal_places)
    return xunit.any_decimal(min_value=min_value, max_value=max_value, decimal_places=decimal_places)