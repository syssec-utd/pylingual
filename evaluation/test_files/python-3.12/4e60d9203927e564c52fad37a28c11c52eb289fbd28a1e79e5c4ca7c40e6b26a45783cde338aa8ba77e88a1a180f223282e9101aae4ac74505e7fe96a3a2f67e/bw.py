from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.decimal_to_precision import TICK_SIZE

class bw(Exchange):

    def describe(self):
        return self.deep_extend(super(bw, self).describe(), {'id': 'bw', 'name': 'BW', 'countries': ['CN'], 'rateLimit': 1500, 'version': 'v1', 'has': {'CORS': None, 'spot': True, 'margin': None, 'swap': None, 'future': None, 'option': None, 'cancelAllOrders': None, 'cancelOrder': True, 'cancelOrders': None, 'createDepositAddress': None, 'createLimitOrder': True, 'createMarketOrder': None, 'createOrder': True, 'createStopLimitOrder': False, 'createStopMarketOrder': False, 'createStopOrder': False, 'editOrder': None, 'fetchBalance': True, 'fetchBidsAsks': None, 'fetchClosedOrders': True, 'fetchCurrencies': True, 'fetchDepositAddress': True, 'fetchDeposits': True, 'fetchL2OrderBook': None, 'fetchLedger': None, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMyTrades': None, 'fetchOHLCV': True, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchOrderBooks': None, 'fetchOrders': True, 'fetchPositionMode': False, 'fetchTicker': True, 'fetchTickers': True, 'fetchTrades': True, 'fetchTradingFee': False, 'fetchTradingFees': True, 'fetchTradingLimits': None, 'fetchTransactionFees': None, 'fetchTransactions': None, 'fetchWithdrawals': True, 'withdraw': None}, 'timeframes': {'1m': '1M', '5m': '5M', '15m': '15M', '30m': '30M', '1h': '1H', '1d': '1D', '1w': '1W'}, 'hostname': 'bw.com', 'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/69436317-31128c80-0d52-11ea-91d1-eb7bb5818812.jpg', 'api': {'rest': 'https://www.{hostname}'}, 'www': 'https://www.bw.com', 'doc': 'https://github.com/bw-exchange/api_docs_en/wiki', 'fees': 'https://www.bw.com/feesRate', 'referral': 'https://www.bw.com/regGetCommission/N3JuT1R3bWxKTE0'}, 'requiredCredentials': {'apiKey': True, 'secret': True}, 'fees': {'trading': {'tierBased': True, 'percentage': True, 'taker': self.parse_number('0.002'), 'maker': self.parse_number('0.002')}, 'funding': {}}, 'precisionMode': TICK_SIZE, 'exceptions': {'exact': {'999': AuthenticationError, '1000': ExchangeNotAvailable, '2012': OrderNotFound, '5017': BadSymbol, '10001': RateLimitExceeded}}, 'api': {'public': {'get': ['api/data/v1/klines', 'api/data/v1/ticker', 'api/data/v1/tickers', 'api/data/v1/trades', 'api/data/v1/entrusts', 'exchange/config/controller/website/marketcontroller/getByWebId', 'exchange/config/controller/website/currencycontroller/getCurrencyList']}, 'private': {'get': ['exchange/entrust/controller/website/EntrustController/getEntrustById', 'exchange/entrust/controller/website/EntrustController/getUserEntrustRecordFromCacheWithPage', 'exchange/entrust/controller/website/EntrustController/getUserEntrustList', 'exchange/fund/controller/website/fundwebsitecontroller/getwithdrawaddress', 'exchange/fund/controller/website/fundwebsitecontroller/getpayoutcoinrecord', 'exchange/entrust/controller/website/EntrustController/getUserEntrustList'], 'post': ['exchange/fund/controller/website/fundcontroller/getPayinAddress', 'exchange/fund/controller/website/fundcontroller/getPayinCoinRecord', 'exchange/fund/controller/website/fundcontroller/findbypage', 'exchange/entrust/controller/website/EntrustController/addEntrust', 'exchange/entrust/controller/website/EntrustController/cancelEntrust']}}})

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for bw
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.publicGetExchangeConfigControllerWebsiteMarketcontrollerGetByWebId(params)
        markets = self.safe_value(response, 'datas', [])
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = self.safe_string(market, 'marketId')
            numericId = int(id)
            name = self.safe_string_upper(market, 'name')
            base, quote = name.split('_')
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            baseId = self.safe_string(market, 'sellerCurrencyId')
            quoteId = self.safe_string(market, 'buyerCurrencyId')
            state = self.safe_integer(market, 'state')
            fee = self.safe_number(market, 'defaultFee')
            result.append({'id': id, 'numericId': numericId, 'symbol': base + '/' + quote, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'baseNumericId': int(baseId), 'quoteNumericId': int(quoteId), 'type': 'spot', 'spot': True, 'margin': False, 'swap': False, 'future': False, 'option': False, 'active': state == 1, 'contract': False, 'linear': None, 'inverse': None, 'taker': fee, 'maker': fee, 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.parse_number(self.parse_precision(self.safe_string(market, 'amountDecimal'))), 'price': self.parse_number(self.parse_precision(self.safe_string(market, 'priceDecimal')))}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': self.safe_number(market, 'minAmount'), 'max': None}, 'price': {'min': self.parse_number('0'), 'max': None}, 'cost': {'min': self.parse_number('0'), 'max': None}}, 'info': market})
        return result

    def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = self.publicGetExchangeConfigControllerWebsiteCurrencycontrollerGetCurrencyList(params)
        currencies = self.safe_value(response, 'datas', [])
        result = {}
        for i in range(0, len(currencies)):
            currency = currencies[i]
            id = self.safe_string(currency, 'currencyId')
            code = self.safe_currency_code(self.safe_string_upper(currency, 'name'))
            state = self.safe_integer(currency, 'state')
            rechargeFlag = self.safe_integer(currency, 'rechargeFlag')
            drawFlag = self.safe_integer(currency, 'drawFlag')
            deposit = rechargeFlag == 1
            withdraw = drawFlag == 1
            active = state == 1
            result[code] = {'id': id, 'code': code, 'info': currency, 'name': code, 'active': active, 'deposit': deposit, 'withdraw': withdraw, 'fee': self.safe_number(currency, 'drawFee'), 'precision': None, 'limits': {'amount': {'min': self.safe_number(currency, 'limitAmount', 0), 'max': None}, 'withdraw': {'min': None, 'max': self.safe_number(currency, 'onceDrawLimit')}}}
        return result

    def parse_ticker(self, ticker, market=None):
        marketId = self.safe_string(ticker, 0)
        market = self.safe_market(marketId, market)
        symbol = market['symbol']
        timestamp = self.milliseconds()
        close = self.safe_string(ticker, 1)
        bid = self.safe_value(ticker, 'bid', {})
        ask = self.safe_value(ticker, 'ask', {})
        return self.safe_ticker({'symbol': symbol, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'high': self.safe_string(ticker, 2), 'low': self.safe_string(ticker, 3), 'bid': self.safe_string(ticker, 7), 'bidVolume': self.safe_string(bid, 'quantity'), 'ask': self.safe_string(ticker, 8), 'askVolume': self.safe_string(ask, 'quantity'), 'vwap': None, 'open': None, 'close': close, 'last': close, 'previousClose': None, 'change': self.safe_string(ticker, 5), 'percentage': None, 'average': None, 'baseVolume': self.safe_string(ticker, 4), 'quoteVolume': self.safe_string(ticker, 9), 'info': ticker}, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id']}
        response = self.publicGetApiDataV1Ticker(self.extend(request, params))
        ticker = self.safe_value(response, 'datas', [])
        return self.parse_ticker(ticker, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        response = self.publicGetApiDataV1Tickers(params)
        datas = self.safe_value(response, 'datas', [])
        result = {}
        for i in range(0, len(datas)):
            ticker = self.parse_ticker(datas[i])
            symbol = ticker['symbol']
            if symbols is None or self.in_array(symbol, symbols):
                result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id']}
        if limit is not None:
            request['dataSize'] = limit
        response = self.publicGetApiDataV1Entrusts(self.extend(request, params))
        orderbook = self.safe_value(response, 'datas', [])
        timestamp = self.safe_timestamp(orderbook, 'timestamp')
        return self.parse_order_book(orderbook, market['symbol'], timestamp)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 2)
        priceString = self.safe_string(trade, 5)
        amountString = self.safe_string(trade, 6)
        marketId = self.safe_string(trade, 1)
        delimiter = None
        if marketId is not None:
            if not marketId in self.markets_by_id:
                delimiter = '_'
                marketId = self.safe_string(trade, 3)
        market = self.safe_market(marketId, market, delimiter)
        sideString = self.safe_string(trade, 4)
        side = 'sell' if sideString == 'ask' else 'buy'
        return self.safe_trade({'id': None, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': market['symbol'], 'order': None, 'type': 'limit', 'side': side, 'takerOrMaker': None, 'price': priceString, 'amount': amountString, 'cost': None, 'fee': None, 'info': trade}, market)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id']}
        if limit is not None:
            request['dataSize'] = limit
        response = self.publicGetApiDataV1Trades(self.extend(request, params))
        trades = self.safe_value(response, 'datas', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>` indexed by market symbols
        """
        self.load_markets()
        response = self.publicGetExchangeConfigControllerWebsiteMarketcontrollerGetByWebId()
        datas = self.safe_value(response, 'datas', [])
        result = {}
        for i in range(0, len(datas)):
            data = datas[i]
            marketId = self.safe_string(data, 'name')
            symbol = self.safe_symbol(marketId, None, '_')
            fee = self.safe_number(data, 'defaultFee')
            result[symbol] = {'info': data, 'symbol': symbol, 'maker': fee, 'taker': fee, 'percentage': True, 'tierBased': True}
        return result

    def parse_ohlcv(self, ohlcv, market=None):
        return [self.safe_timestamp(ohlcv, 3), self.safe_number(ohlcv, 4), self.safe_number(ohlcv, 5), self.safe_number(ohlcv, 6), self.safe_number(ohlcv, 7), self.safe_number(ohlcv, 8)]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id'], 'type': self.timeframes[timeframe], 'dataSize': 500}
        if limit is not None:
            request['dataSize'] = limit
        response = self.publicGetApiDataV1Klines(self.extend(request, params))
        data = self.safe_value(response, 'datas', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def parse_balance(self, response):
        data = self.safe_value(response, 'datas', {})
        balances = self.safe_value(data, 'list', [])
        result = {'info': response}
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currencyTypeId')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'amount')
            account['used'] = self.safe_string(balance, 'freeze')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privatePostExchangeFundControllerWebsiteFundcontrollerFindbypage(params)
        return self.parse_balance(response)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if price is None:
            raise ExchangeError(self.id + ' createOrder() allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        request = {'amount': self.amount_to_precision(symbol, amount), 'price': self.price_to_precision(symbol, price), 'type': 1 if side == 'buy' else 0, 'rangeType': 0, 'marketId': market['id']}
        response = self.privatePostExchangeEntrustControllerWebsiteEntrustControllerAddEntrust(self.extend(request, params))
        data = self.safe_value(response, 'datas')
        id = self.safe_string(data, 'entrustId')
        return {'id': id, 'info': response, 'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 'symbol': symbol, 'type': type, 'side': side, 'price': price, 'amount': amount, 'cost': None, 'average': None, 'filled': None, 'remaining': None, 'status': 'open', 'fee': None, 'trades': None, 'clientOrderId': None}

    def parse_order_status(self, status):
        statuses = {'-3': 'canceled', '-2': 'canceled', '-1': 'canceled', '0': 'open', '1': 'canceled', '2': 'closed', '3': 'open', '4': 'canceled'}
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        marketId = self.safe_string(order, 'marketId')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.safe_integer(order, 'createTime')
        side = self.safe_string(order, 'type')
        if side == '0':
            side = 'sell'
        elif side == '1':
            side = 'buy'
        amount = self.safe_string(order, 'amount')
        price = self.safe_string(order, 'price')
        filled = self.safe_string(order, 'completeAmount')
        remaining = self.safe_string_2(order, 'availabelAmount', 'availableAmount')
        cost = self.safe_string(order, 'totalMoney')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        return self.safe_order({'info': order, 'id': self.safe_string(order, 'entrustId'), 'clientOrderId': None, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'lastTradeTimestamp': None, 'symbol': symbol, 'type': 'limit', 'timeInForce': None, 'postOnly': None, 'side': side, 'price': price, 'stopPrice': None, 'amount': amount, 'cost': cost, 'average': None, 'filled': filled, 'remaining': remaining, 'status': status, 'fee': None, 'trades': None}, market)

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id'], 'entrustId': id}
        response = self.privateGetExchangeEntrustControllerWebsiteEntrustControllerGetEntrustById(self.extend(request, params))
        order = self.safe_value(response, 'datas', {})
        return self.parse_order(order, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id'], 'entrustId': id}
        response = self.privatePostExchangeEntrustControllerWebsiteEntrustControllerCancelEntrust(self.extend(request, params))
        return {'info': response, 'id': id}

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id']}
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetExchangeEntrustControllerWebsiteEntrustControllerGetUserEntrustRecordFromCacheWithPage(self.extend(request, params))
        data = self.safe_value(response, 'datas', {})
        orders = self.safe_value(data, 'entrustList', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchClosedOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id']}
        if limit is not None:
            request['pageSize'] = limit
        if since is not None:
            request['startDateTime'] = since
        response = self.privateGetExchangeEntrustControllerWebsiteEntrustControllerGetUserEntrustList(self.extend(request, params))
        data = self.safe_value(response, 'datas', {})
        orders = self.safe_value(data, 'entrustList', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'marketId': market['id']}
        if since is not None:
            request['startDateTime'] = since
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetExchangeEntrustControllerWebsiteEntrustControllerGetUserEntrustList(self.extend(request, params))
        data = self.safe_value(response, 'datas', {})
        orders = self.safe_value(data, 'entrustList', [])
        return self.parse_orders(orders, market, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.implode_hostname(self.urls['api']['rest']) + '/' + path
        if method == 'GET':
            if params:
                url += '?' + self.urlencode(params)
        else:
            body = self.json(params)
        if api == 'private':
            ms = str(self.milliseconds())
            content = ''
            if method == 'GET':
                sortedParams = self.keysort(params)
                keys = list(sortedParams.keys())
                for i in range(0, len(keys)):
                    key = keys[i]
                    content += key + str(sortedParams[key])
            else:
                content = body
            signature = self.apiKey + ms + content + self.secret
            hash = self.hash(self.encode(signature), 'md5')
            if not headers:
                headers = {}
            headers['Apiid'] = self.apiKey
            headers['Timestamp'] = ms
            headers['Sign'] = hash
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the bw api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currencyTypeName': currency['name']}
        response = self.privatePostExchangeFundControllerWebsiteFundcontrollerGetPayinAddress(self.extend(request, params))
        data = self.safe_value(response, 'datas', {})
        address = self.safe_string(data, 'address')
        tag = self.safe_string(data, 'memo')
        self.check_address(address)
        return {'currency': code, 'address': self.check_address(address), 'tag': tag, 'network': None, 'info': response}

    def parse_transaction_status(self, status):
        statuses = {'-1': 'canceled', '0': 'pending', '1': 'ok'}
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        id = self.safe_string(transaction, 'depositId', 'withdrawalId')
        address = self.safe_string_2(transaction, 'depositAddress', 'withdrawalAddress')
        currencyId = self.safe_string_2(transaction, 'currencyId', 'currencyTypeId')
        code = None
        if currencyId in self.currencies_by_id:
            currency = self.currencies_by_id[currencyId]
        if code is None and currency is not None:
            code = currency['code']
        type = 'deposit' if 'depositId' in transaction else 'withdrawal'
        amount = self.safe_number_2(transaction, 'actuallyAmount', 'amount')
        status = self.parse_transaction_status(self.safe_string_2(transaction, 'verifyStatus', 'state'))
        timestamp = self.safe_integer(transaction, 'createTime')
        txid = self.safe_string(transaction, 'txId')
        fee = None
        feeCost = self.safe_number(transaction, 'fees')
        if feeCost is not None:
            fee = {'cost': feeCost, 'currency': code}
        return {'info': transaction, 'id': id, 'txid': txid, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'network': None, 'addressFrom': None, 'address': address, 'addressTo': None, 'tagFrom': None, 'tag': None, 'tagTo': None, 'type': type, 'amount': amount, 'currency': code, 'status': status, 'updated': None, 'fee': fee}

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchDeposits() requires a currency code argument')
        self.load_markets()
        currency = self.currency(code)
        request = {'currencyTypeName': currency['name']}
        if limit is not None:
            request['pageSize'] = limit
        response = self.privatePostExchangeFundControllerWebsiteFundcontrollerGetPayinCoinRecord(self.extend(request, params))
        data = self.safe_value(response, 'datas', {})
        deposits = self.safe_value(data, 'list', [])
        return self.parse_transactions(deposits, code, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the bw api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchWithdrawals() requires a currency code argument')
        self.load_markets()
        currency = self.currency(code)
        request = {'currencyId': currency['id']}
        if limit is not None:
            request['pageSize'] = limit
        response = self.privateGetExchangeFundControllerWebsiteFundwebsitecontrollerGetpayoutcoinrecord(self.extend(request, params))
        data = self.safe_value(response, 'datas', {})
        withdrawals = self.safe_value(data, 'list', [])
        return self.parse_transactions(withdrawals, code, since, limit)

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            return
        resMsg = self.safe_value(response, 'resMsg')
        errorCode = self.safe_string(resMsg, 'code')
        if errorCode != '1':
            feedback = self.id + ' ' + self.json(response)
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
            raise ExchangeError(feedback)