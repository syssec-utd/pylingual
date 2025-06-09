def make_aware(value, timezone=None):
    """
    Make a naive datetime.datetime in a given time zone aware.

    :param value: datetime
    :param timezone: timezone
    :return: localized datetime in settings.TIMEZONE or timezone

    """
    if timezone is None:
        timezone = TIMEZONE
    if is_localized(value):
        raise ValueError('make_aware expects a naive datetime, got %s' % value)
    if hasattr(value, 'fold'):
        value = value.replace(fold=1)
    if hasattr(timezone, 'localize'):
        return timezone.localize(value)
    elif hasattr(timezone, 'convert'):
        return timezone.convert(value)
    else:
        return value.replace(tzinfo=timezone)