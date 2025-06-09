def date_field_data(field, **kwargs):
    """
    Return random value for DateField

    >>> result = any_form_field(forms.DateField())
    >>> type(result)
    <type 'str'>
    """
    from_date = kwargs.get('from_date', date(1990, 1, 1))
    to_date = kwargs.get('to_date', date.today())
    date_format = random.choice(field.input_formats or formats.get_format('DATE_INPUT_FORMATS'))
    return xunit.any_date(from_date=from_date, to_date=to_date).strftime(date_format)