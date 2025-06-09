def _get_url(self, ticker, frequency):
    """
        Return url based on frequency.  Daily, weekly, or yearly use Tiingo
        EOD api; anything less than daily uses the iex intraday api.
        :param ticker (string): ticker to be embedded in the url
        :param frequency (string): valid frequency per Tiingo api
        :return (string): url
        """
    if self._invalid_frequency(frequency):
        etext = 'Error: {} is an invalid frequency.  Check Tiingo API documentation for valid EOD or intraday frequency format.'
        raise InvalidFrequencyError(etext.format(frequency))
    elif self._is_eod_frequency(frequency):
        return 'tiingo/daily/{}/prices'.format(ticker)
    else:
        return 'iex/{}/prices'.format(ticker)