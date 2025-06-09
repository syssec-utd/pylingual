def prune(self, symbol: SecuritySymbol):
    """
        Delete all but the latest available price for the given symbol.
        Returns the number of items removed.
        """
    from .repositories import PriceRepository
    assert isinstance(symbol, SecuritySymbol)
    self.logger.debug(f'pruning prices for {symbol}')
    repo = PriceRepository()
    query = repo.query.filter(dal.Price.namespace == symbol.namespace).filter(dal.Price.symbol == symbol.mnemonic).order_by(dal.Price.date.desc()).order_by(dal.Price.time.desc())
    all_prices = query.all()
    deleted = False
    first = True
    for single in all_prices:
        if not first:
            repo.query.filter(dal.Price.id == single.id).delete()
            deleted = True
            self.logger.debug(f'deleting {single.id}')
        else:
            first = False
    repo.save()
    return deleted