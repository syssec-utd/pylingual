def nature(self, nature):
    """
        Sets the nature of this YearlyFinancials.
        Nature of the balancesheet

        :param nature: The nature of this YearlyFinancials.
        :type: str
        """
    allowed_values = ['STANDALONE']
    if nature not in allowed_values:
        raise ValueError('Invalid value for `nature`, must be one of {0}'.format(allowed_values))
    self._nature = nature