def subscribe_to_ticker(self, pair, **kwargs):
    """Subscribe to the passed pair's ticker channel.

        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
    identifier = ('ticker', pair)
    self._subscribe('ticker', identifier, symbol=pair, **kwargs)