def _get_rate(self, currency, date):
    """Get a rate for a given currency and date.

        :type date: datetime.date

        >>> from datetime import date
        >>> c = CurrencyConverter()
        >>> c._get_rate('USD', date=date(2014, 3, 28))
        1.375...
        >>> c._get_rate('BGN', date=date(2010, 11, 21))
        Traceback (most recent call last):
        RateNotFoundError: BGN has no rate for 2010-11-21
        """
    if currency == self.ref_currency:
        return 1.0
    if date not in self._rates[currency]:
        first_date, last_date = self.bounds[currency]
        if not self.fallback_on_wrong_date:
            raise RateNotFoundError('{0} not in {1} bounds {2}/{3}'.format(date, currency, first_date, last_date))
        if date < first_date:
            fallback_date = first_date
        elif date > last_date:
            fallback_date = last_date
        else:
            raise AssertionError('Should never happen, bug in the code!')
        if self.verbose:
            print('/!\\ {0} not in {1} bounds {2}/{3}, falling back to {4}'.format(date, currency, first_date, last_date, fallback_date))
        date = fallback_date
    rate = self._rates[currency][date]
    if rate is None:
        raise RateNotFoundError('{0} has no rate for {1}'.format(currency, date))
    return rate