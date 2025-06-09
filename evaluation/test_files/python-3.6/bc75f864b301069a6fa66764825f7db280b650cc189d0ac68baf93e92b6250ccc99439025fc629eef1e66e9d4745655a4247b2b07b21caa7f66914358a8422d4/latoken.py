from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import AccountSuspended
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import TICK_SIZE

class latoken(Exchange):

    def describe(self):
        return self.deep_extend(super(latoken, self).describe(), {'id': 'latoken', 'name': 'Latoken', 'countries': ['KY'], 'version': 'v2', 'rateLimit': 1000, 'has': {'CORS': None, 'spot': True, 'margin': False, 'swap': None, 'future': None, 'option': False, 'cancelAllOrders': True, 'cancelOrder': True, 'createOrder': True, 'fetchBalance': True, 'fetchBorrowRate': False, 'fetchBorrowRateHistories': False, 'fetchBorrowRateHistory': False, 'fetchBorrowRates': False, 'fetchBorrowRatesPerSymbol': False, 'fetchCurrencies': True, 'fetchDepositWithdrawFees': False, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMyTrades': True, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchOrders': True, 'fetchPositionMode': False, 'fetchTicker': True, 'fetchTickers': True, 'fetchTime': True, 'fetchTrades': True, 'fetchTradingFee': True, 'fetchTradingFees': False, 'fetchTransactions': True, 'fetchTransfer': False, 'fetchTransfers': True, 'transfer': True}, 'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/61511972-24c39f00-aa01-11e9-9f7c-471f1d6e5214.jpg', 'api': {'rest': 'https://api.latoken.com'}, 'www': 'https://latoken.com', 'doc': ['https://api.latoken.com'], 'fees': 'https://latoken.com/fees', 'referral': 'https://latoken.com/invite?r=mvgp2djk'}, 'api': {'public': {'get': {'book/{currency}/{quote}': 1, 'chart/week': 1, 'chart/week/{currency}/{quote}': 1, 'currency': 1, 'currency/available': 1, 'currency/quotes': 1, 'currency/{currency}': 1, 'pair': 1, 'pair/available': 1, 'ticker': 1, 'ticker/{base}/{quote}': 1, 'time': 1, 'trade/history/{currency}/{quote}': 1, 'trade/fee/{currency}/{quote}': 1, 'trade/feeLevels': 1, 'transaction/bindings': 1}}, 'private': {'get': {'auth/account': 1, 'auth/account/currency/{currency}/{type}': 1, 'auth/order': 1, 'auth/order/getOrder/{id}': 1, 'auth/order/pair/{currency}/{quote}': 1, 'auth/order/pair/{currency}/{quote}/active': 1, 'auth/stopOrder': 1, 'auth/stopOrder/getOrder/{id}': 1, 'auth/stopOrder/pair/{currency}/{quote}': 1, 'auth/stopOrder/pair/{currency}/{quote}/active': 1, 'auth/trade': 1, 'auth/trade/pair/{currency}/{quote}': 1, 'auth/trade/fee/{currency}/{quote}': 1, 'auth/transaction': 1, 'auth/transaction/bindings': 1, 'auth/transaction/bindings/{currency}': 1, 'auth/transaction/{id}': 1, 'auth/transfer': 1}, 'post': {'auth/order/cancel': 1, 'auth/order/cancelAll': 1, 'auth/order/cancelAll/{currency}/{quote}': 1, 'auth/order/place': 1, 'auth/spot/deposit': 1, 'auth/spot/withdraw': 1, 'auth/stopOrder/cancel': 1, 'auth/stopOrder/cancelAll': 1, 'auth/stopOrder/cancelAll/{currency}/{quote}': 1, 'auth/stopOrder/place': 1, 'auth/transaction/depositAddress': 1, 'auth/transaction/withdraw': 1, 'auth/transaction/withdraw/cancel': 1, 'auth/transaction/withdraw/confirm': 1, 'auth/transaction/withdraw/resendCode': 1, 'auth/transfer/email': 1, 'auth/transfer/id': 1, 'auth/transfer/phone': 1}}}, 'precisionMode': TICK_SIZE, 'fees': {'trading': {'feeSide': 'get', 'tierBased': False, 'percentage': True, 'maker': self.parse_number('0.0049'), 'taker': self.parse_number('0.0049')}}, 'commonCurrencies': {'BUX': 'Buxcoin', 'CBT': 'Community Business Token', 'CTC': 'CyberTronchain', 'DMD': 'Diamond Coin', 'FREN': 'Frenchie', 'GDX': 'GoldenX', 'GEC': 'Geco One', 'GEM': 'NFTmall', 'GMT': 'GMT Token', 'IMC': 'IMCoin', 'MT': 'Monarch', 'TPAY': 'Tetra Pay', 'TRADE': 'Smart Trade Coin', 'TSL': 'Treasure SL', 'UNO': 'Unobtanium', 'WAR': 'Warrior Token'}, 'exceptions': {'exact': {'INTERNAL_ERROR': ExchangeError, 'SERVICE_UNAVAILABLE': ExchangeNotAvailable, 'NOT_AUTHORIZED': AuthenticationError, 'FORBIDDEN': PermissionDenied, 'BAD_REQUEST': BadRequest, 'NOT_FOUND': ExchangeError, 'ACCESS_DENIED': PermissionDenied, 'REQUEST_REJECTED': ExchangeError, 'HTTP_MEDIA_TYPE_NOT_SUPPORTED': BadRequest, 'MEDIA_TYPE_NOT_ACCEPTABLE': BadRequest, 'METHOD_ARGUMENT_NOT_VALID': BadRequest, 'VALIDATION_ERROR': BadRequest, 'ACCOUNT_EXPIRED': AccountSuspended, 'BAD_CREDENTIALS': AuthenticationError, 'COOKIE_THEFT': AuthenticationError, 'CREDENTIALS_EXPIRED': AccountSuspended, 'INSUFFICIENT_AUTHENTICATION': AuthenticationError, 'UNKNOWN_LOCATION': AuthenticationError, 'TOO_MANY_REQUESTS': RateLimitExceeded, 'INSUFFICIENT_FUNDS': InsufficientFunds, 'ORDER_VALIDATION': InvalidOrder, 'BAD_TICKS': InvalidOrder}, 'broad': {'invalid API key, signature or digest': AuthenticationError, 'The API key was revoked': AuthenticationError, 'request expired or bad': InvalidNonce, 'For input string': BadRequest, 'Unable to resolve currency by tag': BadSymbol, "Can't find currency with tag": BadSymbol, 'Unable to place order because pair is in inactive state': BadSymbol, 'API keys are not available for FROZEN user': AccountSuspended}}, 'options': {'defaultType': 'spot', 'types': {'wallet': 'ACCOUNT_TYPE_WALLET', 'spot': 'ACCOUNT_TYPE_SPOT'}, 'accounts': {'ACCOUNT_TYPE_WALLET': 'wallet', 'ACCOUNT_TYPE_SPOT': 'spot'}, 'fetchTradingFee': {'method': 'fetchPrivateTradingFee'}}})

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        response = self.publicGetTime(params)
        return self.safe_integer(response, 'serverTime')

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for latoken
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        currencies = self.fetch_currencies_from_cache(params)
        response = self.publicGetPair(params)
        if self.safe_value(self.options, 'adjustForTimeDifference', True):
            self.load_time_difference()
        currenciesById = self.index_by(currencies, 'id')
        result = []
        for i in range(0, len(response)):
            market = response[i]
            id = self.safe_string(market, 'id')
            baseId = self.safe_string(market, 'baseCurrency')
            quoteId = self.safe_string(market, 'quoteCurrency')
            baseCurrency = self.safe_value(currenciesById, baseId)
            quoteCurrency = self.safe_value(currenciesById, quoteId)
            if baseCurrency is not None and quoteCurrency is not None:
                base = self.safe_currency_code(self.safe_string(baseCurrency, 'tag'))
                quote = self.safe_currency_code(self.safe_string(quoteCurrency, 'tag'))
                lowercaseQuote = quote.lower()
                capitalizedQuote = self.capitalize(lowercaseQuote)
                status = self.safe_string(market, 'status')
                result.append({'id': id, 'symbol': base + '/' + quote, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'type': 'spot', 'spot': True, 'margin': False, 'swap': False, 'future': False, 'option': False, 'active': status == 'PAIR_STATUS_ACTIVE', 'contract': False, 'linear': None, 'inverse': None, 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.safe_number(market, 'quantityTick'), 'price': self.safe_number(market, 'priceTick')}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': self.safe_number(market, 'minOrderQuantity'), 'max': None}, 'price': {'min': None, 'max': None}, 'cost': {'min': self.safe_number(market, 'minOrderCost' + capitalizedQuote), 'max': self.safe_number(market, 'maxOrderCost' + capitalizedQuote)}}, 'info': market})
        return result

    def fetch_currencies_from_cache(self, params={}):
        options = self.safe_value(self.options, 'fetchCurrencies', {})
        timestamp = self.safe_integer(options, 'timestamp')
        expires = self.safe_integer(options, 'expires', 1000)
        now = self.milliseconds()
        if timestamp is None or now - timestamp > expires:
            response = self.publicGetCurrency(params)
            self.options['fetchCurrencies'] = self.extend(options, {'response': response, 'timestamp': now})
        return self.safe_value(self.options['fetchCurrencies'], 'response')

    def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = self.fetch_currencies_from_cache(params)
        result = {}
        for i in range(0, len(response)):
            currency = response[i]
            id = self.safe_string(currency, 'id')
            tag = self.safe_string(currency, 'tag')
            code = self.safe_currency_code(tag)
            fee = self.safe_number(currency, 'fee')
            currencyType = self.safe_string(currency, 'type')
            parts = currencyType.split('_')
            numParts = len(parts)
            lastPart = self.safe_value(parts, numParts - 1)
            type = lastPart.lower()
            status = self.safe_string(currency, 'status')
            active = status == 'CURRENCY_STATUS_ACTIVE'
            name = self.safe_string(currency, 'name')
            result[code] = {'id': id, 'code': code, 'info': currency, 'name': name, 'type': type, 'active': active, 'deposit': None, 'withdraw': None, 'fee': fee, 'precision': self.parse_number(self.parse_precision(self.safe_string(currency, 'decimals'))), 'limits': {'amount': {'min': self.safe_number(currency, 'minTransferAmount'), 'max': None}, 'withdraw': {'min': None, 'max': None}}}
        return result

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privateGetAuthAccount(params)
        result = {'info': response, 'timestamp': None, 'datetime': None}
        maxTimestamp = None
        defaultType = self.safe_string_2(self.options, 'fetchBalance', 'defaultType', 'spot')
        type = self.safe_string(params, 'type', defaultType)
        types = self.safe_value(self.options, 'types', {})
        accountType = self.safe_string(types, type, type)
        balancesByType = self.group_by(response, 'type')
        balances = self.safe_value(balancesByType, accountType, [])
        for i in range(0, len(balances)):
            balance = balances[i]
            currencyId = self.safe_string(balance, 'currency')
            timestamp = self.safe_integer(balance, 'timestamp')
            if timestamp is not None:
                if maxTimestamp is None:
                    maxTimestamp = timestamp
                else:
                    maxTimestamp = max(maxTimestamp, timestamp)
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'available')
            account['used'] = self.safe_string(balance, 'blocked')
            result[code] = account
        result['timestamp'] = maxTimestamp
        result['datetime'] = self.iso8601(maxTimestamp)
        return self.safe_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['baseId'], 'quote': market['quoteId']}
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetBookCurrencyQuote(self.extend(request, params))
        return self.parse_order_book(response, symbol, None, 'bid', 'ask', 'price', 'quantity')

    def parse_ticker(self, ticker, market=None):
        marketId = self.safe_string(ticker, 'symbol')
        symbol = self.safe_symbol(marketId, market)
        last = self.safe_string(ticker, 'lastPrice')
        change = self.safe_string(ticker, 'change24h')
        timestamp = self.nonce()
        return self.safe_ticker({'symbol': symbol, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'low': self.safe_string(ticker, 'low'), 'high': self.safe_string(ticker, 'high'), 'bid': None, 'bidVolume': None, 'ask': None, 'askVolume': None, 'vwap': None, 'open': None, 'close': last, 'last': last, 'previousClose': None, 'change': change, 'percentage': None, 'average': None, 'baseVolume': None, 'quoteVolume': self.safe_string(ticker, 'volume24h'), 'info': ticker}, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'base': market['baseId'], 'quote': market['quoteId']}
        response = self.publicGetTickerBaseQuote(self.extend(request, params))
        return self.parse_ticker(response, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        response = self.publicGetTicker(params)
        return self.parse_tickers(response, symbols)

    def parse_trade(self, trade, market=None):
        type = None
        timestamp = self.safe_integer(trade, 'timestamp')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'quantity')
        costString = self.safe_string(trade, 'cost')
        makerBuyer = self.safe_value(trade, 'makerBuyer')
        side = self.safe_string(trade, 'direction')
        if side is None:
            side = 'sell' if makerBuyer else 'buy'
        elif side == 'TRADE_DIRECTION_BUY':
            side = 'buy'
        elif side == 'TRADE_DIRECTION_SELL':
            side = 'sell'
        isBuy = side == 'buy'
        takerOrMaker = 'maker' if makerBuyer and isBuy else 'taker'
        baseId = self.safe_string(trade, 'baseCurrency')
        quoteId = self.safe_string(trade, 'quoteCurrency')
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        symbol = base + '/' + quote
        if symbol in self.markets:
            market = self.market(symbol)
        id = self.safe_string(trade, 'id')
        orderId = self.safe_string(trade, 'order')
        feeCost = self.safe_string(trade, 'fee')
        fee = None
        if feeCost is not None:
            fee = {'cost': feeCost, 'currency': quote}
        return self.safe_trade({'info': trade, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': symbol, 'id': id, 'order': orderId, 'type': type, 'takerOrMaker': takerOrMaker, 'side': side, 'price': priceString, 'amount': amountString, 'cost': costString, 'fee': fee}, market)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['baseId'], 'quote': market['quoteId']}
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetTradeHistoryCurrencyQuote(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_trading_fee(self, symbol, params={}):
        """
        fetch the trading fees for a market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        method = self.safe_string(params, 'method')
        params = self.omit(params, 'method')
        if method is None:
            options = self.safe_value(self.options, 'fetchTradingFee', {})
            method = self.safe_string(options, 'method', 'fetchPrivateTradingFee')
        return getattr(self, method)(symbol, params)

    def fetch_public_trading_fee(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['baseId'], 'quote': market['quoteId']}
        response = self.publicGetTradeFeeCurrencyQuote(self.extend(request, params))
        return {'info': response, 'symbol': market['symbol'], 'maker': self.safe_number(response, 'makerFee'), 'taker': self.safe_number(response, 'takerFee')}

    def fetch_private_trading_fee(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['baseId'], 'quote': market['quoteId']}
        response = self.privateGetAuthTradeFeeCurrencyQuote(self.extend(request, params))
        return {'info': response, 'symbol': market['symbol'], 'maker': self.safe_number(response, 'makerFee'), 'taker': self.safe_number(response, 'takerFee')}

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        self.load_markets()
        request = {}
        method = 'privateGetAuthTrade'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['currency'] = market['baseId']
            request['quote'] = market['quoteId']
            method = 'privateGetAuthTradePairCurrencyQuote'
        if limit is not None:
            request['limit'] = limit
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order_status(self, status):
        statuses = {'ORDER_STATUS_PLACED': 'open', 'ORDER_STATUS_CLOSED': 'closed', 'ORDER_STATUS_CANCELLED': 'canceled'}
        return self.safe_string(statuses, status, status)

    def parse_order_type(self, status):
        statuses = {'ORDER_TYPE_MARKET': 'market', 'ORDER_TYPE_LIMIT': 'limit'}
        return self.safe_string(statuses, status, status)

    def parse_time_in_force(self, timeInForce):
        timeInForces = {'ORDER_CONDITION_GOOD_TILL_CANCELLED': 'GTC', 'ORDER_CONDITION_IMMEDIATE_OR_CANCEL': 'IOC', 'ORDER_CONDITION_FILL_OR_KILL': 'FOK'}
        return self.safe_string(timeInForces, timeInForce, timeInForce)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        timestamp = self.safe_integer(order, 'timestamp')
        baseId = self.safe_string(order, 'baseCurrency')
        quoteId = self.safe_string(order, 'quoteCurrency')
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        symbol = None
        if base is not None and quote is not None:
            symbol = base + '/' + quote
            if symbol in self.markets:
                market = self.market(symbol)
        orderSide = self.safe_string(order, 'side')
        side = None
        if orderSide is not None:
            parts = orderSide.split('_')
            partsLength = len(parts)
            side = self.safe_string_lower(parts, partsLength - 1)
        type = self.parse_order_type(self.safe_string(order, 'type'))
        price = self.safe_string(order, 'price')
        amount = self.safe_string(order, 'quantity')
        filled = self.safe_string(order, 'filled')
        cost = self.safe_string(order, 'cost')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        message = self.safe_string(order, 'message')
        if message is not None:
            if message.find('cancel') >= 0:
                status = 'canceled'
            elif message.find('accept') >= 0:
                status = 'open'
        clientOrderId = self.safe_string(order, 'clientOrderId')
        timeInForce = self.parse_time_in_force(self.safe_string(order, 'condition'))
        return self.safe_order({'id': id, 'clientOrderId': clientOrderId, 'info': order, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'lastTradeTimestamp': None, 'status': status, 'symbol': symbol, 'type': type, 'timeInForce': timeInForce, 'postOnly': None, 'side': side, 'price': price, 'stopPrice': None, 'triggerPrice': None, 'cost': cost, 'amount': amount, 'filled': filled, 'average': None, 'remaining': None, 'fee': None, 'trades': None}, market)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {'currency': market['baseId'], 'quote': market['quoteId']}
        response = self.privateGetAuthOrderPairCurrencyQuoteActive(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        method = 'privateGetAuthOrder'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['currency'] = market['baseId']
            request['quote'] = market['quoteId']
            method = 'privateGetAuthOrderPairCurrencyQuote'
        if limit is not None:
            request['limit'] = limit
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_orders(response, market, since, limit)

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: not used by latoken fetchOrder
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {'id': id}
        response = self.privateGetAuthOrderGetOrderId(self.extend(request, params))
        return self.parse_order(response)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        uppercaseType = type.upper()
        request = {'baseCurrency': market['baseId'], 'quoteCurrency': market['quoteId'], 'side': side.upper(), 'condition': 'GTC', 'type': uppercaseType, 'clientOrderId': self.uuid()}
        if uppercaseType == 'LIMIT':
            request['price'] = self.price_to_precision(symbol, price)
        request['quantity'] = self.amount_to_precision(symbol, amount)
        request['timestamp'] = self.seconds()
        response = self.privatePostAuthOrderPlace(self.extend(request, params))
        return self.parse_order(response, market)

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: not used by latoken cancelOrder()
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {'id': id}
        response = self.privatePostAuthOrderCancel(self.extend(request, params))
        return self.parse_order(response)

    def cancel_all_orders(self, symbol=None, params={}):
        """
        cancel all open orders in a market
        :param str symbol: unified market symbol of the market to cancel orders in
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        method = 'privatePostAuthOrderCancelAll'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['currency'] = market['baseId']
            request['quote'] = market['quoteId']
            method = 'privatePostAuthOrderCancelAllCurrencyQuote'
        response = getattr(self, method)(self.extend(request, params))
        return response

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        """
        fetch history of deposits and withdrawals
        :param str|None code: unified currency code for the currency of the transactions, default is None
        :param int|None since: timestamp in ms of the earliest transaction, default is None
        :param int|None limit: max number of transactions to return, default is None
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: a list of `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        response = self.privateGetAuthTransaction(self.extend(request, params))
        currency = None
        if code is not None:
            currency = self.currency(code)
        content = self.safe_value(response, 'content', [])
        return self.parse_transactions(content, currency, since, limit)

    def parse_transaction(self, transaction, currency=None):
        id = self.safe_string(transaction, 'id')
        timestamp = self.safe_integer(transaction, 'timestamp')
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        amount = self.safe_number(transaction, 'amount')
        addressFrom = self.safe_string(transaction, 'senderAddress')
        addressTo = self.safe_string(transaction, 'recipientAddress')
        txid = self.safe_string(transaction, 'transactionHash')
        tagTo = self.safe_string(transaction, 'memo')
        fee = None
        feeCost = self.safe_number(transaction, 'transactionFee')
        if feeCost is not None:
            fee = {'cost': feeCost, 'currency': code}
        type = self.parse_transaction_type(self.safe_string(transaction, 'type'))
        return {'info': transaction, 'id': id, 'txid': txid, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'network': None, 'addressFrom': addressFrom, 'addressTo': addressTo, 'address': addressTo, 'tagFrom': None, 'tagTo': tagTo, 'tag': tagTo, 'type': type, 'amount': amount, 'currency': code, 'status': status, 'updated': None, 'fee': fee}

    def parse_transaction_status(self, status):
        statuses = {'TRANSACTION_STATUS_CONFIRMED': 'ok', 'TRANSACTION_STATUS_EXECUTED': 'ok', 'TRANSACTION_STATUS_CANCELLED': 'canceled'}
        return self.safe_string(statuses, status, status)

    def parse_transaction_type(self, type):
        types = {'TRANSACTION_TYPE_DEPOSIT': 'deposit', 'TRANSACTION_TYPE_WITHDRAWAL': 'withdrawal'}
        return self.safe_string(types, type, type)

    def fetch_transfers(self, code=None, since=None, limit=None, params={}):
        """
        fetch a history of internal transfers made on an account
        :param str|None code: unified currency code of the currency transferred
        :param int|None since: the earliest time in ms to fetch transfers for
        :param int|None limit: the maximum number of  transfers structures to retrieve
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns [dict]: a list of `transfer structures <https://docs.ccxt.com/en/latest/manual.html#transfer-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        response = self.privateGetAuthTransfer(params)
        transfers = self.safe_value(response, 'content', [])
        return self.parse_transfers(transfers, currency, since, limit)

    def transfer(self, code, amount, fromAccount, toAccount, params={}):
        """
        transfer currency internally between wallets on the same account
        :param str code: unified currency code
        :param float amount: amount to transfer
        :param str fromAccount: account to transfer from
        :param str toAccount: account to transfer to
        :param dict params: extra parameters specific to the latoken api endpoint
        :returns dict: a `transfer structure <https://docs.ccxt.com/en/latest/manual.html#transfer-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        method = None
        if toAccount.find('@') >= 0:
            method = 'privatePostAuthTransferEmail'
        elif len(toAccount) == 36:
            method = 'privatePostAuthTransferId'
        else:
            method = 'privatePostAuthTransferPhone'
        request = {'currency': currency['id'], 'recipient': toAccount, 'value': self.currency_to_precision(code, amount)}
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_transfer(response)

    def parse_transfer(self, transfer, currency=None):
        timestamp = self.safe_timestamp(transfer, 'timestamp')
        currencyId = self.safe_string(transfer, 'currency')
        status = self.safe_string(transfer, 'status')
        return {'info': transfer, 'id': self.safe_string(transfer, 'id'), 'timestamp': self.safe_integer(transfer, 'timestamp'), 'datetime': self.iso8601(timestamp), 'currency': self.safe_currency_code(currencyId, currency), 'amount': self.safe_number(transfer, 'transferringFunds'), 'fromAccount': self.safe_string(transfer, 'fromAccount'), 'toAccount': self.safe_string(transfer, 'toAccount'), 'status': self.parse_transfer_status(status)}

    def parse_transfer_status(self, status):
        statuses = {'TRANSFER_STATUS_COMPLETED': 'ok', 'TRANSFER_STATUS_PENDING': 'pending', 'TRANSFER_STATUS_REJECTED': 'failed', 'TRANSFER_STATUS_UNVERIFIED': 'pending', 'TRANSFER_STATUS_CANCELLED': 'canceled'}
        return self.safe_string(statuses, status, status)

    def sign(self, path, api='public', method='GET', params=None, headers=None, body=None):
        request = '/' + self.version + '/' + self.implode_params(path, params)
        requestString = request
        query = self.omit(params, self.extract_params(path))
        urlencodedQuery = self.urlencode(query)
        if method == 'GET':
            if query:
                requestString += '?' + urlencodedQuery
        if api == 'private':
            self.check_required_credentials()
            auth = method + request + urlencodedQuery
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512)
            headers = {'X-LA-APIKEY': self.apiKey, 'X-LA-SIGNATURE': signature, 'X-LA-DIGEST': 'HMAC-SHA512'}
            if method == 'POST':
                headers['Content-Type'] = 'application/json'
                body = self.json(query)
        url = self.urls['api']['rest'] + requestString
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            return
        message = self.safe_string(response, 'message')
        feedback = self.id + ' ' + body
        if message is not None:
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
        error = self.safe_value(response, 'error')
        errorMessage = self.safe_string(error, 'message')
        if error is not None or errorMessage is not None:
            self.throw_exactly_matched_exception(self.exceptions['exact'], error, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)
            raise ExchangeError(feedback)