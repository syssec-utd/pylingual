def _value__get(self):
    """
        Get/set the value of this select (the selected option).

        If this is a multi-select, this is a set-like object that
        represents all the selected options.
        """
    if self.multiple:
        return MultipleSelectOptions(self)
    for el in _options_xpath(self):
        if el.get('selected') is not None:
            value = el.get('value')
            if value is None:
                value = el.text or ''
            if value:
                value = value.strip()
            return value
    return None