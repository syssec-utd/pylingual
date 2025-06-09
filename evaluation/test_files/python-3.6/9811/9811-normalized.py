def _set_missing_to_none(self, currency):
    """Fill missing rates of a currency with the closest available ones."""
    rates = self._rates[currency]
    (first_date, last_date) = self.bounds[currency]
    for date in list_dates_between(first_date, last_date):
        if date not in rates:
            rates[date] = None
    if self.verbose:
        missing = len([r for r in itervalues(rates) if r is None])
        if missing:
            print('{0}: {1} missing rates from {2} to {3} ({4} days)'.format(currency, missing, first_date, last_date, 1 + (last_date - first_date).days))