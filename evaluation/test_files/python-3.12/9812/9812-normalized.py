def _compute_missing_rates(self, currency):
    """Fill missing rates of a currency.

        This is done by linear interpolation of the two closest available rates.

        :param str currency: The currency to fill missing rates for.
        """
    rates = self._rates[currency]
    tmp = defaultdict(lambda: [None, None])
    for date in sorted(rates):
        rate = rates[date]
        if rate is not None:
            closest_rate = rate
            dist = 0
        else:
            dist += 1
            tmp[date][0] = (closest_rate, dist)
    for date in sorted(rates, reverse=True):
        rate = rates[date]
        if rate is not None:
            closest_rate = rate
            dist = 0
        else:
            dist += 1
            tmp[date][1] = (closest_rate, dist)
    for date in sorted(tmp):
        (r0, d0), (r1, d1) = tmp[date]
        rates[date] = (r0 * d1 + r1 * d0) / (d0 + d1)
        if self.verbose:
            print('{0}: filling {1} missing rate using {2} ({3}d old) and {4} ({5}d later)'.format(currency, date, r0, d0, r1, d1))