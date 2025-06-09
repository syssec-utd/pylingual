from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import AddressPending
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import OnMaintenance
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import TICK_SIZE

class bittrex(Exchange):

    def describe(self):
        return self.deep_extend(super(bittrex, self).describe(), {'id': 'bittrex', 'name': 'Bittrex', 'countries': ['US'], 'version': 'v3', 'rateLimit': 1500, 'certified': False, 'pro': True, 'has': {'CORS': None, 'spot': True, 'margin': False, 'swap': False, 'future': False, 'option': False, 'addMargin': False, 'cancelAllOrders': True, 'cancelOrder': True, 'createDepositAddress': True, 'createMarketOrder': True, 'createOrder': True, 'createReduceOnlyOrder': False, 'createStopLimitOrder': True, 'createStopMarketOrder': True, 'createStopOrder': True, 'fetchBalance': True, 'fetchBidsAsks': True, 'fetchBorrowRate': False, 'fetchBorrowRateHistories': False, 'fetchBorrowRateHistory': False, 'fetchBorrowRates': False, 'fetchBorrowRatesPerSymbol': False, 'fetchClosedOrders': True, 'fetchCurrencies': True, 'fetchDeposit': True, 'fetchDepositAddress': True, 'fetchDeposits': True, 'fetchFundingHistory': False, 'fetchFundingRate': False, 'fetchFundingRateHistory': False, 'fetchFundingRates': False, 'fetchIndexOHLCV': False, 'fetchLeverage': False, 'fetchLeverageTiers': False, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMarkOHLCV': False, 'fetchMyTrades': True, 'fetchOHLCV': True, 'fetchOpenInterestHistory': False, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchOrderTrades': True, 'fetchPosition': False, 'fetchPositionMode': False, 'fetchPositions': False, 'fetchPositionsRisk': False, 'fetchPremiumIndexOHLCV': False, 'fetchTicker': True, 'fetchTickers': True, 'fetchTime': True, 'fetchTrades': True, 'fetchTradingFee': True, 'fetchTradingFees': True, 'fetchTransactionFees': None, 'fetchTransactions': None, 'fetchWithdrawal': True, 'fetchWithdrawals': True, 'reduceMargin': False, 'setLeverage': False, 'setMarginMode': False, 'setPositionMode': False, 'withdraw': True}, 'timeframes': {'1m': 'MINUTE_1', '5m': 'MINUTE_5', '1h': 'HOUR_1', '1d': 'DAY_1'}, 'hostname': 'bittrex.com', 'urls': {'logo': 'https://user-images.githubusercontent.com/51840849/87153921-edf53180-c2c0-11ea-96b9-f2a9a95a455b.jpg', 'api': {'public': 'https://api.bittrex.com', 'private': 'https://api.bittrex.com'}, 'www': 'https://bittrex.com', 'doc': ['https://bittrex.github.io/api/v3'], 'fees': ['https://bittrex.zendesk.com/hc/en-us/articles/115003684371-BITTREX-SERVICE-FEES-AND-WITHDRAWAL-LIMITATIONS', 'https://bittrex.zendesk.com/hc/en-us/articles/115000199651-What-fees-does-Bittrex-charge-'], 'referral': 'https://bittrex.com/Account/Register?referralCode=1ZE-G0G-M3B'}, 'api': {'public': {'get': ['ping', 'currencies', 'currencies/{symbol}', 'markets', 'markets/tickers', 'markets/summaries', 'markets/{marketSymbol}', 'markets/{marketSymbol}/summary', 'markets/{marketSymbol}/orderbook', 'markets/{marketSymbol}/trades', 'markets/{marketSymbol}/ticker', 'markets/{marketSymbol}/candles/{candleInterval}/recent', 'markets/{marketSymbol}/candles/{candleInterval}/historical/{year}/{month}/{day}', 'markets/{marketSymbol}/candles/{candleInterval}/historical/{year}/{month}', 'markets/{marketSymbol}/candles/{candleInterval}/historical/{year}']}, 'private': {'get': ['account', 'account/fees/fiat', 'account/fees/fiat/{currencySymbol}', 'account/fees/trading', 'account/fees/trading/{marketSymbol}', 'account/volume', 'account/permissions/markets', 'account/permissions/markets/{marketSymbol}', 'account/permissions/currencies', 'account/permissions/currencies/{currencySymbol}', 'addresses', 'addresses/{currencySymbol}', 'balances', 'balances/{currencySymbol}', 'deposits/open', 'deposits/closed', 'deposits/ByTxId/{txId}', 'deposits/{depositId}', 'executions', 'executions/last-id', 'executions/{executionId}', 'orders/closed', 'orders/open', 'orders/{orderId}', 'orders/{orderId}/executions', 'ping', 'subaccounts/{subaccountId}', 'subaccounts', 'subaccounts/withdrawals/open', 'subaccounts/withdrawals/closed', 'subaccounts/deposits/open', 'subaccounts/deposits/closed', 'withdrawals/open', 'withdrawals/closed', 'withdrawals/ByTxId/{txId}', 'withdrawals/{withdrawalId}', 'withdrawals/allowed-addresses', 'conditional-orders/{conditionalOrderId}', 'conditional-orders/closed', 'conditional-orders/open', 'transfers/sent', 'transfers/received', 'transfers/{transferId}', 'funds-transfer-methods/{fundsTransferMethodId}'], 'post': ['addresses', 'orders', 'subaccounts', 'withdrawals', 'conditional-orders', 'transfers', 'batch'], 'delete': ['orders/open', 'orders/{orderId}', 'withdrawals/{withdrawalId}', 'conditional-orders/{conditionalOrderId}']}}, 'fees': {'trading': {'tierBased': True, 'percentage': True, 'maker': self.parse_number('0.0075'), 'taker': self.parse_number('0.0075')}, 'funding': {'tierBased': False, 'percentage': False}}, 'precisionMode': TICK_SIZE, 'exceptions': {'exact': {'BAD_REQUEST': BadRequest, 'STARTDATE_OUT_OF_RANGE': BadRequest, 'APISIGN_NOT_PROVIDED': AuthenticationError, 'APIKEY_INVALID': AuthenticationError, 'INVALID_SIGNATURE': AuthenticationError, 'INVALID_CURRENCY': ExchangeError, 'INVALID_PERMISSION': AuthenticationError, 'INSUFFICIENT_FUNDS': InsufficientFunds, 'INVALID_CEILING_MARKET_BUY': InvalidOrder, 'INVALID_FIAT_ACCOUNT': InvalidOrder, 'INVALID_ORDER_TYPE': InvalidOrder, 'QUANTITY_NOT_PROVIDED': InvalidOrder, 'MIN_TRADE_REQUIREMENT_NOT_MET': InvalidOrder, 'NOT_FOUND': OrderNotFound, 'ORDER_NOT_OPEN': OrderNotFound, 'INVALID_ORDER': InvalidOrder, 'UUID_INVALID': OrderNotFound, 'RATE_NOT_PROVIDED': InvalidOrder, 'INVALID_MARKET': BadSymbol, 'WHITELIST_VIOLATION_IP': PermissionDenied, 'DUST_TRADE_DISALLOWED_MIN_VALUE': InvalidOrder, 'RESTRICTED_MARKET': BadSymbol, 'We are down for scheduled maintenance, but we’ll be back up shortly.': OnMaintenance}, 'broad': {'throttled': DDoSProtection, 'problem': ExchangeNotAvailable}}, 'options': {'fetchTicker': {'method': 'publicGetMarketsMarketSymbolTicker'}, 'fetchTickers': {'method': 'publicGetMarketsTickers'}, 'fetchDeposits': {'status': 'ok'}, 'fetchWithdrawals': {'status': 'ok'}, 'parseOrderStatus': False, 'hasAlreadyAuthenticatedSuccessfully': False, 'tag': {'NXT': True, 'CRYPTO_NOTE_PAYMENTID': True, 'BITSHAREX': True, 'RIPPLE': True, 'NEM': True, 'STELLAR': True, 'STEEM': True}, 'subaccountId': None, 'fetchClosedOrdersFilterBySince': True}, 'commonCurrencies': {'BIFI': 'Bifrost Finance', 'BTR': 'BTRIPS', 'GMT': 'GMT Token', 'MEME': 'Memetic', 'MER': 'Mercury', 'PROS': 'Pros.Finance', 'REPV2': 'REP', 'TON': 'Tokamak Network'}})

    def fee_to_precision(self, symbol, fee):
        return self.decimal_to_precision(fee, TRUNCATE, self.markets[symbol]['precision']['price'], self.precisionMode)

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for bittrex
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.publicGetMarkets(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            baseId = self.safe_string(market, 'baseCurrencySymbol')
            quoteId = self.safe_string(market, 'quoteCurrencySymbol')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            status = self.safe_string(market, 'status')
            result.append({'id': self.safe_string(market, 'symbol'), 'symbol': base + '/' + quote, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'type': 'spot', 'spot': True, 'margin': False, 'swap': False, 'future': False, 'option': False, 'active': status == 'ONLINE', 'contract': False, 'linear': None, 'inverse': None, 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.parse_number('1e-8'), 'price': self.parse_number(self.parse_precision(self.safe_string(market, 'precision')))}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': self.safe_number(market, 'minTradeSize'), 'max': None}, 'price': {'min': None, 'max': None}, 'cost': {'min': None, 'max': None}}, 'info': market})
        return result

    def parse_balance(self, response):
        result = {'info': response}
        indexed = self.index_by(response, 'currencySymbol')
        currencyIds = list(indexed.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            balance = indexed[currencyId]
            account['free'] = self.safe_string(balance, 'available')
            account['total'] = self.safe_string(balance, 'total')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privateGetBalances(params)
        return self.parse_balance(response)

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketSymbol': market['id']}
        if limit is not None:
            if limit != 1 and limit != 25 and (limit != 500):
                raise BadRequest(self.id + ' fetchOrderBook() limit argument must be None, 1, 25 or 500, default is 25')
            request['depth'] = limit
        response = self.publicGetMarketsMarketSymbolOrderbook(self.extend(request, params))
        sequence = self.safe_integer(self.last_response_headers, 'Sequence')
        orderbook = self.parse_order_book(response, market['symbol'], None, 'bid', 'ask', 'rate', 'quantity')
        orderbook['nonce'] = sequence
        return orderbook

    def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = self.publicGetCurrencies(params)
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_string(currency, 'symbol')
            code = self.safe_currency_code(id)
            precision = self.parse_number('1e-8')
            fee = self.safe_number(currency, 'txFee')
            isActive = self.safe_string(currency, 'status')
            result[code] = {'id': id, 'code': code, 'address': self.safe_string(currency, 'baseAddress'), 'info': currency, 'type': self.safe_string(currency, 'coinType'), 'name': self.safe_string(currency, 'name'), 'active': isActive == 'ONLINE', 'deposit': None, 'withdraw': None, 'fee': fee, 'precision': precision, 'limits': {'amount': {'min': precision, 'max': None}, 'withdraw': {'min': fee, 'max': None}}}
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.parse8601(self.safe_string(ticker, 'updatedAt'))
        marketId = self.safe_string(ticker, 'symbol')
        market = self.safe_market(marketId, market, '-')
        symbol = market['symbol']
        percentage = self.safe_string(ticker, 'percentChange')
        last = self.safe_string(ticker, 'lastTradeRate')
        return self.safe_ticker({'symbol': symbol, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'high': self.safe_string(ticker, 'high'), 'low': self.safe_string(ticker, 'low'), 'bid': self.safe_string(ticker, 'bidRate'), 'bidVolume': None, 'ask': self.safe_string(ticker, 'askRate'), 'askVolume': None, 'vwap': None, 'open': None, 'close': last, 'last': last, 'previousClose': None, 'change': None, 'percentage': percentage, 'average': None, 'baseVolume': self.safe_string(ticker, 'volume'), 'quoteVolume': self.safe_string(ticker, 'quoteVolume'), 'info': ticker}, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        options = self.safe_value(self.options, 'fetchTickers', {})
        defaultMethod = self.safe_string(options, 'method', 'publicGetMarketsTickers')
        method = self.safe_string(params, 'method', defaultMethod)
        params = self.omit(params, 'method')
        response = getattr(self, method)(params)
        tickers = []
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            tickers.append(ticker)
        return self.filter_by_array(tickers, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketSymbol': market['id']}
        options = self.safe_value(self.options, 'fetchTicker', {})
        defaultMethod = self.safe_string(options, 'method', 'publicGetMarketsMarketSymbolTicker')
        method = self.safe_string(params, 'method', defaultMethod)
        params = self.omit(params, 'method')
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_bids_asks(self, symbols=None, params={}):
        """
        fetches the bid and ask price and volume for multiple markets
        :param [str]|None symbols: unified symbols of the markets to fetch the bids and asks for, all markets are returned if not assigned
        :param dict params: extra parameters specific to the binance api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        response = self.publicGetMarketsTickers(params)
        return self.parse_tickers(response, symbols)

    def parse_trade(self, trade, market=None):
        timestamp = self.parse8601(self.safe_string(trade, 'executedAt'))
        id = self.safe_string(trade, 'id')
        order = self.safe_string(trade, 'orderId')
        marketId = self.safe_string(trade, 'marketSymbol')
        market = self.safe_market(marketId, market, '-')
        priceString = self.safe_string(trade, 'rate')
        amountString = self.safe_string(trade, 'quantity')
        takerOrMaker = None
        side = self.safe_string_lower_2(trade, 'takerSide', 'direction')
        isTaker = self.safe_value(trade, 'isTaker')
        if isTaker is not None:
            takerOrMaker = 'taker' if isTaker else 'maker'
            if not isTaker:
                if side == 'buy':
                    side = 'sell'
                elif side == 'sell':
                    side = 'buy'
        fee = None
        feeCostString = self.safe_string(trade, 'commission')
        if feeCostString is not None:
            fee = {'cost': feeCostString, 'currency': market['quote']}
        return self.safe_trade({'info': trade, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': market['symbol'], 'id': id, 'order': order, 'takerOrMaker': takerOrMaker, 'type': None, 'side': side, 'price': priceString, 'amount': amountString, 'cost': None, 'fee': fee}, market)

    def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        response = self.publicGetPing(params)
        return self.safe_integer(response, 'serverTime')

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketSymbol': market['id']}
        response = self.publicGetMarketsMarketSymbolTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_trading_fee(self, symbol, params={}):
        """
        fetch the trading fees for a market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'marketSymbol': market['id']}
        response = self.privateGetAccountFeesTradingMarketSymbol(self.extend(request, params))
        return self.parse_trading_fee(response, market)

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>` indexed by market symbols
        """
        self.load_markets()
        response = self.privateGetAccountFeesTrading(params)
        return self.parse_trading_fees(response)

    def parse_trading_fee(self, fee, market=None):
        marketId = self.safe_string(fee, 'marketSymbol')
        maker = self.safe_number(fee, 'makerRate')
        taker = self.safe_number(fee, 'takerRate')
        return {'info': fee, 'symbol': self.safe_symbol(marketId, market), 'maker': maker, 'taker': taker}

    def parse_trading_fees(self, fees):
        result = {'info': fees}
        for i in range(0, len(fees)):
            fee = self.parse_trading_fee(fees[i])
            symbol = fee['symbol']
            result[symbol] = fee
        return result

    def parse_ohlcv(self, ohlcv, market=None):
        return [self.parse8601(self.safe_string(ohlcv, 'startsAt')), self.safe_number(ohlcv, 'open'), self.safe_number(ohlcv, 'high'), self.safe_number(ohlcv, 'low'), self.safe_number(ohlcv, 'close'), self.safe_number(ohlcv, 'volume')]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        reverseId = market['baseId'] + '-' + market['quoteId']
        request = {'candleInterval': self.timeframes[timeframe], 'marketSymbol': reverseId}
        method = 'publicGetMarketsMarketSymbolCandlesCandleIntervalRecent'
        if since is not None:
            now = self.milliseconds()
            difference = abs(now - since)
            sinceDate = self.yyyymmdd(since)
            parts = sinceDate.split('-')
            sinceYear = self.safe_integer(parts, 0)
            sinceMonth = self.safe_integer(parts, 1)
            sinceDay = self.safe_integer(parts, 2)
            if timeframe == '1d':
                if difference > 31622400000:
                    method = 'publicGetMarketsMarketSymbolCandlesCandleIntervalHistoricalYear'
                    request['year'] = sinceYear
            elif timeframe == '1h':
                if difference > 2678400000:
                    method = 'publicGetMarketsMarketSymbolCandlesCandleIntervalHistoricalYearMonth'
                    request['year'] = sinceYear
                    request['month'] = sinceMonth
            elif difference > 86400000:
                method = 'publicGetMarketsMarketSymbolCandlesCandleIntervalHistoricalYearMonthDay'
                request['year'] = sinceYear
                request['month'] = sinceMonth
                request['day'] = sinceDay
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        market = None
        stop = self.safe_value(params, 'stop')
        if symbol is not None:
            market = self.market(symbol)
            request['marketSymbol'] = market['id']
        method = 'privateGetOrdersOpen'
        if stop:
            method = 'privateGetConditionalOrdersOpen'
        query = self.omit(params, 'stop')
        response = getattr(self, method)(self.extend(request, query))
        return self.parse_orders(response, market, since, limit)

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        """
        fetch all the trades made from a single order
        :param str id: order id
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        self.load_markets()
        request = {'orderId': id}
        response = self.privateGetOrdersOrderIdExecutions(self.extend(request, params))
        market = None
        if symbol is not None:
            market = self.market(symbol)
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        uppercaseType = None
        if type is not None:
            uppercaseType = type.upper()
        reverseId = market['baseId'] + '-' + market['quoteId']
        stop = self.safe_value(params, 'stop')
        stopPrice = self.safe_number_2(params, 'triggerPrice', 'stopPrice')
        request = {'marketSymbol': reverseId}
        method = 'privatePostOrders'
        if stop or stopPrice:
            method = 'privatePostConditionalOrders'
            operand = self.safe_string(params, 'operand')
            if operand is None:
                raise ArgumentsRequired(self.id + ' createOrder() requires an operand parameter')
            trailingStopPercent = self.safe_number(params, 'trailingStopPercent')
            orderToCreate = self.safe_value(params, 'orderToCreate')
            orderToCancel = self.safe_value(params, 'orderToCancel')
            if stopPrice is None:
                request['trailingStopPercent'] = self.price_to_precision(symbol, trailingStopPercent)
            if orderToCreate:
                isCeilingLimit = uppercaseType == 'CEILING_LIMIT'
                isCeilingMarket = uppercaseType == 'CEILING_MARKET'
                isCeilingOrder = isCeilingLimit or isCeilingMarket
                ceiling = None
                limit = None
                timeInForce = None
                if isCeilingOrder:
                    cost = None
                    if isCeilingLimit:
                        limit = self.price_to_precision(symbol, price)
                        cost = self.safe_number_2(params, 'ceiling', 'cost', amount)
                    elif isCeilingMarket:
                        cost = self.safe_number_2(params, 'ceiling', 'cost')
                        if cost is None:
                            if price is None:
                                cost = amount
                            else:
                                cost = amount * price
                    ceiling = self.cost_to_precision(symbol, cost)
                    timeInForce = 'IMMEDIATE_OR_CANCEL'
                elif uppercaseType == 'LIMIT':
                    limit = self.price_to_precision(symbol, price)
                    timeInForce = 'GOOD_TIL_CANCELLED'
                else:
                    timeInForce = 'IMMEDIATE_OR_CANCEL'
                request['orderToCreate'] = {'marketSymbol': reverseId, 'direction': side.upper(), 'type': uppercaseType, 'quantity': self.amount_to_precision(symbol, amount), 'ceiling': ceiling, 'limit': limit, 'timeInForce': timeInForce, 'clientOrderId': self.safe_string(params, 'clientOrderId'), 'useAwards': self.safe_value(params, 'useAwards')}
            if orderToCancel:
                request['orderToCancel'] = orderToCancel
            request['triggerPrice'] = self.price_to_precision(symbol, stopPrice)
            request['operand'] = operand
        else:
            if side is not None:
                request['direction'] = side.upper()
            request['type'] = uppercaseType
            isCeilingLimit = uppercaseType == 'CEILING_LIMIT'
            isCeilingMarket = uppercaseType == 'CEILING_MARKET'
            isCeilingOrder = isCeilingLimit or isCeilingMarket
            if isCeilingOrder:
                cost = None
                if isCeilingLimit:
                    request['limit'] = self.price_to_precision(symbol, price)
                    cost = self.safe_number_2(params, 'ceiling', 'cost', amount)
                elif isCeilingMarket:
                    cost = self.safe_number_2(params, 'ceiling', 'cost')
                    if cost is None:
                        if price is None:
                            cost = amount
                        else:
                            cost = amount * price
                request['ceiling'] = self.cost_to_precision(symbol, cost)
                request['timeInForce'] = 'IMMEDIATE_OR_CANCEL'
            else:
                request['quantity'] = self.amount_to_precision(symbol, amount)
                if uppercaseType == 'LIMIT':
                    request['limit'] = self.price_to_precision(symbol, price)
                    request['timeInForce'] = 'GOOD_TIL_CANCELLED'
                else:
                    request['timeInForce'] = 'IMMEDIATE_OR_CANCEL'
        query = self.omit(params, ['stop', 'stopPrice', 'ceiling', 'cost', 'operand', 'trailingStopPercent', 'orderToCreate', 'orderToCancel'])
        response = getattr(self, method)(self.extend(request, query))
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        stop = self.safe_value(params, 'stop')
        request = {}
        method = None
        market = None
        if symbol is not None:
            market = self.market(symbol)
        if stop:
            method = 'privateDeleteConditionalOrdersConditionalOrderId'
            request = {'conditionalOrderId': id}
        else:
            method = 'privateDeleteOrdersOrderId'
            request = {'orderId': id}
        query = self.omit(params, 'stop')
        response = getattr(self, method)(self.extend(request, query))
        return self.extend(self.parse_order(response, market), {'id': id, 'info': response, 'status': 'canceled'})

    def cancel_all_orders(self, symbol=None, params={}):
        """
        cancel all open orders
        :param str|None symbol: unified market symbol, only orders in the market of self symbol are cancelled when symbol is not None
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['marketSymbol'] = market['id']
        response = self.privateDeleteOrdersOpen(self.extend(request, params))
        orders = []
        for i in range(0, len(response)):
            result = self.safe_value(response[i], 'result', {})
            orders.append(result)
        return self.parse_orders(orders, market)

    def fetch_deposit(self, id, code=None, params={}):
        """
        fetch data on a currency deposit via the deposit id
        :param str id: deposit id
        :param str|None code: filter by currency code
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {'txId': id}
        currency = None
        if code is not None:
            currency = self.currency(code)
        response = self.privateGetDepositsByTxIdTxId(self.extend(request, params))
        transactions = self.parse_transactions(response, currency, None, None)
        return self.safe_value(transactions, 0)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :param int|None params['endDate']: Filters out result after self timestamp. Uses ISO-8602 format.
        :param str|None params['nextPageToken']: The unique identifier of the item that the resulting query result should start after, in the sort order of the given endpoint. Used for traversing a paginated set in the forward direction.
        :param str|None params['previousPageToken']: The unique identifier of the item that the resulting query result should end before, in the sort order of the given endpoint. Used for traversing a paginated set in the reverse direction.
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currencySymbol'] = currency['id']
        if since is not None:
            startDate = int(since / 1000) * 1000
            request['startDate'] = self.iso8601(startDate)
        if limit is not None:
            request['pageSize'] = limit
        method = None
        options = self.safe_value(self.options, 'fetchDeposits', {})
        defaultStatus = self.safe_string(options, 'status', 'ok')
        status = self.safe_string(params, 'status', defaultStatus)
        if status == 'pending':
            method = 'privateGetDepositsOpen'
        else:
            method = 'privateGetDepositsClosed'
        params = self.omit(params, 'status')
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_transactions(response, currency, None, limit)

    def fetch_pending_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all pending deposits made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :param int|None params['endDate']: Filters out result after self timestamp. Uses ISO-8602 format.
        :param str|None params['nextPageToken']: The unique identifier of the item that the resulting query result should start after, in the sort order of the given endpoint. Used for traversing a paginated set in the forward direction.
        :param str|None params['previousPageToken']: The unique identifier of the item that the resulting query result should end before, in the sort order of the given endpoint. Used for traversing a paginated set in the reverse direction.
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        return self.fetch_deposits(code, since, limit, self.extend(params, {'status': 'pending'}))

    def fetch_withdrawal(self, id, code=None, params={}):
        """
        fetch data on a currency withdrawal via the withdrawal id
        :param str id: withdrawal id
        :param str|None code: filter by currency code
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {'txId': id}
        currency = None
        if code is not None:
            currency = self.currency(code)
        response = self.privateGetWithdrawalsByTxIdTxId(self.extend(request, params))
        transactions = self.parse_transactions(response, currency, None, None)
        return self.safe_value(transactions, 0)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :param int|None params['endDate']: Filters out result after self timestamp. Uses ISO-8602 format.
        :param str|None params['nextPageToken']: The unique identifier of the item that the resulting query result should start after, in the sort order of the given endpoint. Used for traversing a paginated set in the forward direction.
        :param str|None params['previousPageToken']: The unique identifier of the item that the resulting query result should end before, in the sort order of the given endpoint. Used for traversing a paginated set in the reverse direction.
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currencySymbol'] = currency['id']
        if since is not None:
            startDate = int(since / 1000) * 1000
            request['startDate'] = self.iso8601(startDate)
        if limit is not None:
            request['pageSize'] = limit
        method = None
        options = self.safe_value(self.options, 'fetchWithdrawals', {})
        defaultStatus = self.safe_string(options, 'status', 'ok')
        status = self.safe_string(params, 'status', defaultStatus)
        if status == 'pending':
            method = 'privateGetWithdrawalsOpen'
        else:
            method = 'privateGetWithdrawalsClosed'
        params = self.omit(params, 'status')
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_transactions(response, currency, since, limit)

    def fetch_pending_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all pending withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :param int|None params['endDate']: Filters out result after self timestamp. Uses ISO-8602 format.
        :param str|None params['nextPageToken']: The unique identifier of the item that the resulting query result should start after, in the sort order of the given endpoint. Used for traversing a paginated set in the forward direction.
        :param str|None params['previousPageToken']: The unique identifier of the item that the resulting query result should end before, in the sort order of the given endpoint. Used for traversing a paginated set in the reverse direction.
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        return self.fetch_withdrawals(code, since, limit, self.extend(params, {'status': 'pending'}))

    def parse_transaction(self, transaction, currency=None):
        id = self.safe_string_2(transaction, 'id', 'clientWithdrawalId')
        amount = self.safe_number(transaction, 'quantity')
        address = self.safe_string(transaction, 'cryptoAddress')
        addressTo = None
        addressFrom = None
        isDeposit = self.safe_string(transaction, 'source') == 'BLOCKCHAIN'
        if isDeposit:
            addressFrom = address
        else:
            addressTo = address
        txid = self.safe_string(transaction, 'txId')
        updated = self.parse8601(self.safe_string(transaction, 'updatedAt'))
        opened = self.parse8601(self.safe_string(transaction, 'createdAt'))
        timestamp = opened if opened else updated
        type = 'deposit' if opened is None else 'withdrawal'
        currencyId = self.safe_string(transaction, 'currencySymbol')
        code = self.safe_currency_code(currencyId, currency)
        status = 'pending'
        if type == 'deposit':
            status = 'ok'
        else:
            responseStatus = self.safe_string(transaction, 'status')
            if responseStatus == 'ERROR_INVALID_ADDRESS':
                status = 'failed'
            elif responseStatus == 'CANCELLED':
                status = 'canceled'
            elif responseStatus == 'PENDING':
                status = 'pending'
            elif responseStatus == 'COMPLETED':
                status = 'ok'
            elif responseStatus == 'AUTHORIZED' and txid is not None:
                status = 'ok'
        feeCost = self.safe_number(transaction, 'txCost')
        if feeCost is None:
            if type == 'deposit':
                feeCost = 0
        return {'info': transaction, 'id': id, 'currency': code, 'amount': amount, 'network': None, 'address': address, 'addressTo': addressTo, 'addressFrom': addressFrom, 'tag': None, 'tagTo': None, 'tagFrom': None, 'status': status, 'type': type, 'updated': updated, 'txid': txid, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'fee': {'currency': code, 'cost': feeCost}}

    def parse_time_in_force(self, timeInForce):
        timeInForces = {'GOOD_TIL_CANCELLED': 'GTC', 'IMMEDIATE_OR_CANCEL': 'IOC', 'FILL_OR_KILL': 'FOK', 'POST_ONLY_GOOD_TIL_CANCELLED': 'PO'}
        return self.safe_string(timeInForces, timeInForce, timeInForce)

    def parse_order(self, order, market=None):
        marketSymbol = self.safe_string(order, 'marketSymbol')
        market = self.safe_market(marketSymbol, market, '-')
        symbol = market['symbol']
        feeCurrency = market['quote']
        createdAt = self.safe_string(order, 'createdAt')
        updatedAt = self.safe_string(order, 'updatedAt')
        closedAt = self.safe_string(order, 'closedAt')
        clientOrderId = self.safe_string(order, 'clientOrderId')
        lastTradeTimestamp = None
        if closedAt is not None:
            lastTradeTimestamp = self.parse8601(closedAt)
        elif updatedAt:
            lastTradeTimestamp = self.parse8601(updatedAt)
        timestamp = self.parse8601(createdAt)
        direction = self.safe_string_lower(order, 'direction')
        if direction is None:
            conditionalOrder = self.safe_value(order, 'orderToCreate')
            if conditionalOrder is None:
                conditionalOrder = self.safe_value(order, 'orderToCancel')
            direction = self.safe_string_lower(conditionalOrder, 'direction')
        type = self.safe_string_lower(order, 'type')
        if type is None:
            conditionalOrder = self.safe_value(order, 'orderToCreate')
            if conditionalOrder is None:
                conditionalOrder = self.safe_value(order, 'orderToCancel')
            type = self.safe_string_lower(conditionalOrder, 'type')
        quantity = self.safe_string(order, 'quantity')
        if quantity is None:
            conditionalOrder = self.safe_value(order, 'orderToCreate')
            if conditionalOrder is None:
                conditionalOrder = self.safe_value(order, 'orderToCancel')
            quantity = self.safe_string(conditionalOrder, 'quantity')
        limit = self.safe_string(order, 'limit')
        if limit is None:
            conditionalOrder = self.safe_value(order, 'orderToCreate')
            if conditionalOrder is None:
                conditionalOrder = self.safe_value(order, 'orderToCancel')
            limit = self.safe_string(conditionalOrder, 'limit')
        timeInForce = self.parse_time_in_force(self.safe_string(order, 'timeInForce'))
        if timeInForce is None:
            conditionalOrder = self.safe_value(order, 'orderToCreate')
            if conditionalOrder is None:
                conditionalOrder = self.safe_value(order, 'orderToCancel')
            timeInForce = self.parse_time_in_force(self.safe_string(conditionalOrder, 'timeInForce'))
        fillQuantity = self.safe_string(order, 'fillQuantity')
        commission = self.safe_number(order, 'commission')
        proceeds = self.safe_string(order, 'proceeds')
        status = self.safe_string_lower(order, 'status')
        postOnly = timeInForce == 'PO'
        return self.safe_order({'id': self.safe_string(order, 'id'), 'clientOrderId': clientOrderId, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'lastTradeTimestamp': lastTradeTimestamp, 'symbol': symbol, 'type': type, 'timeInForce': timeInForce, 'postOnly': postOnly, 'side': direction, 'price': limit, 'stopPrice': self.safe_string(order, 'triggerPrice'), 'cost': proceeds, 'average': None, 'amount': quantity, 'filled': fillQuantity, 'remaining': None, 'status': status, 'fee': {'cost': commission, 'currency': feeCurrency}, 'info': order, 'trades': None}, market)

    def parse_orders(self, orders, market=None, since=None, limit=None, params={}):
        if self.options['fetchClosedOrdersFilterBySince']:
            return super(bittrex, self).parse_orders(orders, market, since, limit, params)
        else:
            return super(bittrex, self).parse_orders(orders, market, None, limit, params)

    def parse_order_status(self, status):
        statuses = {'CLOSED': 'closed', 'OPEN': 'open', 'CANCELLED': 'canceled', 'CANCELED': 'canceled'}
        return self.safe_string(statuses, status, status)

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        stop = self.safe_value(params, 'stop')
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = None
        method = None
        try:
            request = {}
            if stop:
                method = 'privateGetConditionalOrdersConditionalOrderId'
                request['conditionalOrderId'] = id
            else:
                method = 'privateGetOrdersOrderId'
                request['orderId'] = id
            query = self.omit(params, 'stop')
            response = getattr(self, method)(self.extend(request, query))
        except Exception as e:
            if self.last_json_response:
                message = self.safe_string(self.last_json_response, 'message')
                if message == 'UUID_INVALID':
                    raise OrderNotFound(self.id + ' fetchOrder() error: ' + self.last_http_response)
            raise e
        return self.parse_order(response, market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        self.load_markets()
        request = {}
        if limit is not None:
            request['pageSize'] = limit
        if since is not None:
            request['startDate'] = self.ymdhms(since, 'T') + 'Z'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
            request['marketSymbol'] = market['id']
        response = self.privateGetExecutions(self.extend(request, params))
        trades = self.parse_trades(response, market)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        stop = self.safe_value(params, 'stop')
        request = {}
        if limit is not None:
            request['pageSize'] = limit
        if since is not None:
            request['startDate'] = self.ymdhms(since, 'T') + 'Z'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['marketSymbol'] = market['base'] + '-' + market['quote']
        method = 'privateGetOrdersClosed'
        if stop:
            method = 'privateGetConditionalOrdersClosed'
        query = self.omit(params, 'stop')
        response = getattr(self, method)(self.extend(request, query))
        return self.parse_orders(response, market, since, limit)

    def create_deposit_address(self, code, params={}):
        """
        create a currency deposit address
        :param str code: unified currency code of the currency for the deposit address
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currencySymbol': currency['id']}
        response = self.privatePostAddresses(self.extend(request, params))
        address = self.safe_string(response, 'cryptoAddress')
        message = self.safe_string(response, 'status')
        if not address or message == 'REQUESTED':
            raise AddressPending(self.id + ' the address for ' + code + ' is being generated(pending, not ready yet, retry again later)')
        tag = self.safe_string(response, 'cryptoAddressTag')
        if tag is None and currency['type'] in self.options['tag']:
            tag = address
            address = currency['address']
        self.check_address(address)
        return {'currency': code, 'address': address, 'tag': tag, 'info': response}

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currencySymbol': currency['id']}
        response = self.privateGetAddressesCurrencySymbol(self.extend(request, params))
        address = self.safe_string(response, 'cryptoAddress')
        message = self.safe_string(response, 'status')
        if not address or message == 'REQUESTED':
            raise AddressPending(self.id + ' the address for ' + code + ' is being generated(pending, not ready yet, retry again later)')
        tag = self.safe_string(response, 'cryptoAddressTag')
        if tag is None and currency['type'] in self.options['tag']:
            tag = address
            address = currency['address']
        self.check_address(address)
        return {'currency': code, 'address': address, 'tag': tag, 'network': None, 'info': response}

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the bittrex api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        (tag, params) = self.handle_withdraw_tag_and_params(tag, params)
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {'currencySymbol': currency['id'], 'quantity': amount, 'cryptoAddress': address}
        if tag is not None:
            request['cryptoAddressTag'] = tag
        response = self.privatePostWithdrawals(self.extend(request, params))
        return self.parse_transaction(response, currency)

    def sign(self, path, api='v3', method='GET', params={}, headers=None, body=None):
        url = self.implode_params(self.urls['api'][api], {'hostname': self.hostname}) + '/'
        if api == 'private':
            url += self.version + '/'
            self.check_required_credentials()
            url += self.implode_params(path, params)
            params = self.omit(params, self.extract_params(path))
            hashString = ''
            if method == 'POST':
                body = self.json(params)
                hashString = body
            elif params:
                url += '?' + self.rawencode(params)
            contentHash = self.hash(self.encode(hashString), 'sha512', 'hex')
            timestamp = str(self.milliseconds())
            auth = timestamp + url + method + contentHash
            subaccountId = self.safe_value(self.options, 'subaccountId')
            if subaccountId is not None:
                auth += subaccountId
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            headers = {'Api-Key': self.apiKey, 'Api-Timestamp': timestamp, 'Api-Content-Hash': contentHash, 'Api-Signature': signature}
            if subaccountId is not None:
                headers['Api-Subaccount-Id'] = subaccountId
            if method == 'POST':
                headers['Content-Type'] = 'application/json'
        else:
            if api == 'public':
                url += self.version + '/'
            url += self.implode_params(path, params)
            params = self.omit(params, self.extract_params(path))
            if params:
                url += '?' + self.urlencode(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if body[0] == '{':
            feedback = self.id + ' ' + body
            success = self.safe_value(response, 'success')
            if success is None:
                code = self.safe_string(response, 'code')
                if code == 'NOT_FOUND' and url.find('addresses') >= 0:
                    raise InvalidAddress(feedback)
                if code is not None:
                    self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
                    self.throw_broadly_matched_exception(self.exceptions['broad'], code, feedback)
                return
            if isinstance(success, str):
                success = success == 'true'
            if not success:
                message = self.safe_string(response, 'message')
                if message == 'APIKEY_INVALID':
                    if self.options['hasAlreadyAuthenticatedSuccessfully']:
                        raise DDoSProtection(feedback)
                    else:
                        raise AuthenticationError(feedback)
                if message == 'INVALID_ORDER':
                    cancel = 'cancel'
                    indexOfCancel = url.find(cancel)
                    if indexOfCancel >= 0:
                        urlParts = url.split('?')
                        numParts = len(urlParts)
                        if numParts > 1:
                            query = urlParts[1]
                            params = query.split('&')
                            numParams = len(params)
                            orderId = None
                            for i in range(0, numParams):
                                param = params[i]
                                keyValue = param.split('=')
                                if keyValue[0] == 'uuid':
                                    orderId = keyValue[1]
                                    break
                            if orderId is not None:
                                raise OrderNotFound(self.id + ' cancelOrder ' + orderId + ' ' + self.json(response))
                            else:
                                raise OrderNotFound(self.id + ' cancelOrder ' + self.json(response))
                self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
                if message is not None:
                    self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
                raise ExchangeError(feedback)