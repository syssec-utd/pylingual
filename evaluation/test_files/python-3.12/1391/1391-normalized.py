def _remove_dict_keys_with_value(dict_, val):
    """Removes `dict` keys which have have `self` as value."""
    return {k: v for k, v in dict_.items() if v is not val}