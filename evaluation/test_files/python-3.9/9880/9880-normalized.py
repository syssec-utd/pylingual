def last(symbol: str):
    """ displays last price, for symbol if provided """
    app = PriceDbApplication()
    if symbol:
        symbol = symbol.upper()
        sec_symbol = SecuritySymbol('', '')
        sec_symbol.parse(symbol)
        latest = app.get_latest_price(sec_symbol)
        assert isinstance(latest, PriceModel)
        print(f'{latest}')
    else:
        latest = app.get_latest_prices()
        for price in latest:
            print(f'{price}')