from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import OnMaintenance
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise

class exmo(Exchange):

    def describe(self):
        return self.deep_extend(super(exmo, self).describe(), {'id': 'exmo', 'name': 'EXMO', 'countries': ['LT'], 'rateLimit': 350, 'version': 'v1.1', 'has': {'CORS': None, 'spot': True, 'margin': True, 'swap': False, 'future': False, 'option': False, 'addMargin': True, 'cancelOrder': True, 'cancelOrders': False, 'createDepositAddress': False, 'createOrder': True, 'createStopLimitOrder': True, 'createStopMarketOrder': True, 'createStopOrder': True, 'fetchAccounts': False, 'fetchBalance': True, 'fetchCanceledOrders': True, 'fetchCurrencies': True, 'fetchDeposit': True, 'fetchDepositAddress': True, 'fetchDeposits': True, 'fetchDepositWithdrawFee': 'emulated', 'fetchDepositWithdrawFees': True, 'fetchFundingHistory': False, 'fetchFundingRate': False, 'fetchFundingRateHistory': False, 'fetchFundingRates': False, 'fetchIndexOHLCV': False, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMarkOHLCV': False, 'fetchMyTrades': True, 'fetchOHLCV': True, 'fetchOpenInterestHistory': False, 'fetchOpenOrders': True, 'fetchOrder': 'emulated', 'fetchOrderBook': True, 'fetchOrderBooks': True, 'fetchOrderTrades': True, 'fetchPositionMode': False, 'fetchPremiumIndexOHLCV': False, 'fetchTicker': True, 'fetchTickers': True, 'fetchTrades': True, 'fetchTradingFee': False, 'fetchTradingFees': True, 'fetchTransactionFees': True, 'fetchTransactions': True, 'fetchTransfer': False, 'fetchTransfers': False, 'fetchWithdrawal': True, 'fetchWithdrawals': True, 'reduceMargin': True, 'setMargin': False, 'transfer': False, 'withdraw': True}, 'timeframes': {'1m': '1', '5m': '5', '15m': '15', '30m': '30', '45m': '45', '1h': '60', '2h': '120', '3h': '180', '4h': '240', '1d': 'D', '1w': 'W', '1M': 'M'}, 'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27766491-1b0ea956-5eda-11e7-9225-40d67b481b8d.jpg', 'api': {'public': 'https://api.exmo.com', 'private': 'https://api.exmo.com', 'web': 'https://exmo.me'}, 'www': 'https://exmo.me', 'referral': 'https://exmo.me/?ref=131685', 'doc': ['https://exmo.me/en/api_doc?ref=131685'], 'fees': 'https://exmo.com/en/docs/fees'}, 'api': {'web': {'get': ['ctrl/feesAndLimits', 'en/docs/fees']}, 'public': {'get': ['currency', 'currency/list/extended', 'order_book', 'pair_settings', 'ticker', 'trades', 'candles_history', 'required_amount', 'payments/providers/crypto/list']}, 'private': {'post': ['user_info', 'order_create', 'order_cancel', 'stop_market_order_create', 'stop_market_order_cancel', 'user_open_orders', 'user_trades', 'user_cancelled_orders', 'order_trades', 'deposit_address', 'withdraw_crypt', 'withdraw_get_txid', 'excode_create', 'excode_load', 'code_check', 'wallet_history', 'wallet_operations', 'margin/user/order/create', 'margin/user/order/update', 'margin/user/order/cancel', 'margin/user/position/close', 'margin/user/position/margin_add', 'margin/user/position/margin_remove', 'margin/currency/list', 'margin/pair/list', 'margin/settings', 'margin/funding/list', 'margin/user/info', 'margin/user/order/list', 'margin/user/order/history', 'margin/user/order/trades', 'margin/user/order/max_quantity', 'margin/user/position/list', 'margin/user/position/margin_remove_info', 'margin/user/position/margin_add_info', 'margin/user/wallet/list', 'margin/user/wallet/history', 'margin/user/trade/list', 'margin/trades', 'margin/liquidation/feed']}}, 'fees': {'trading': {'feeSide': 'get', 'tierBased': True, 'percentage': True, 'maker': self.parse_number('0.004'), 'taker': self.parse_number('0.004')}, 'transaction': {'tierBased': False, 'percentage': False}}, 'options': {'networks': {'ETH': 'ERC20', 'TRX': 'TRC20'}, 'fetchTradingFees': {'method': 'fetchPrivateTradingFees'}, 'margin': {'fillResponseFromRequest': True}}, 'commonCurrencies': {'GMT': 'GMT Token'}, 'precisionMode': TICK_SIZE, 'exceptions': {'exact': {'40005': AuthenticationError, '40009': InvalidNonce, '40015': ExchangeError, '40016': OnMaintenance, '40017': AuthenticationError, '40032': PermissionDenied, '40033': PermissionDenied, '40034': RateLimitExceeded, '50052': InsufficientFunds, '50054': InsufficientFunds, '50304': OrderNotFound, '50173': OrderNotFound, '50277': InvalidOrder, '50319': InvalidOrder, '50321': InvalidOrder, '50381': InvalidOrder}, 'broad': {'range period is too long': BadRequest, 'invalid syntax': BadRequest, 'API rate limit exceeded': RateLimitExceeded}}})

    def modify_margin_helper(self, symbol, amount, type, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {'position_id': market['id'], 'quantity': amount}
        method = None
        if type == 'add':
            method = 'privatePostMarginUserPositionMarginAdd'
        elif type == 'reduce':
            method = 'privatePostMarginUserPositionMarginReduce'
        response = getattr(self, method)(self.extend(request, params))
        margin = self.parse_margin_modification(response, market)
        options = self.safe_value(self.options, 'margin', {})
        fillResponseFromRequest = self.safe_value(options, 'fillResponseFromRequest', True)
        if fillResponseFromRequest:
            margin['type'] = type
            margin['amount'] = amount
        return margin

    def parse_margin_modification(self, data, market=None):
        return {'info': data, 'type': None, 'amount': None, 'code': self.safe_value(market, 'quote'), 'symbol': self.safe_symbol(None, market), 'total': None, 'status': 'ok'}

    def reduce_margin(self, symbol, amount, params={}):
        """
        remove margin from a position
        :param str symbol: unified market symbol
        :param float amount: the amount of margin to remove
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `margin structure <https://docs.ccxt.com/en/latest/manual.html#reduce-margin-structure>`
        """
        return self.modify_margin_helper(symbol, amount, 'reduce', params)

    def add_margin(self, symbol, amount, params={}):
        """
        add margin
        :param str symbol: unified market symbol
        :param float amount: amount of margin to add
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `margin structure <https://docs.ccxt.com/en/latest/manual.html#add-margin-structure>`
        """
        return self.modify_margin_helper(symbol, amount, 'add', params)

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>` indexed by market symbols
        """
        method = self.safe_string(params, 'method')
        params = self.omit(params, 'method')
        if method is None:
            options = self.safe_value(self.options, 'fetchTradingFees', {})
            method = self.safe_string(options, 'method', 'fetchPrivateTradingFees')
        return getattr(self, method)(params)

    def fetch_private_trading_fees(self, params={}):
        self.load_markets()
        response = self.privatePostMarginPairList(params)
        pairs = self.safe_value(response, 'pairs', [])
        result = {}
        for i in range(0, len(pairs)):
            pair = pairs[i]
            marketId = self.safe_string(pair, 'name')
            symbol = self.safe_symbol(marketId, None, '_')
            makerString = self.safe_string(pair, 'trade_maker_fee')
            takerString = self.safe_string(pair, 'trade_taker_fee')
            maker = self.parse_number(Precise.string_div(makerString, '100'))
            taker = self.parse_number(Precise.string_div(takerString, '100'))
            result[symbol] = {'info': pair, 'symbol': symbol, 'maker': maker, 'taker': taker, 'percentage': True, 'tierBased': True}
        return result

    def fetch_public_trading_fees(self, params={}):
        self.load_markets()
        response = self.publicGetPairSettings(params)
        result = {}
        for i in range(0, len(self.symbols)):
            symbol = self.symbols[i]
            market = self.market(symbol)
            fee = self.safe_value(response, market['id'], {})
            makerString = self.safe_string(fee, 'commission_maker_percent')
            takerString = self.safe_string(fee, 'commission_taker_percent')
            maker = self.parse_number(Precise.string_div(makerString, '100'))
            taker = self.parse_number(Precise.string_div(takerString, '100'))
            result[symbol] = {'info': fee, 'symbol': symbol, 'maker': maker, 'taker': taker, 'percentage': True, 'tierBased': True}
        return result

    def parse_fixed_float_value(self, input):
        if input is None or input == '-':
            return None
        if input == '':
            return 0
        isPercentage = input.find('%') >= 0
        parts = input.split(' ')
        value = parts[0].replace('%', '')
        result = float(value)
        if result > 0 and isPercentage:
            raise ExchangeError(self.id + ' parseFixedFloatValue() detected an unsupported non-zero percentage-based fee ' + input)
        return result

    def fetch_transaction_fees(self, codes=None, params={}):
        """
        *DEPRECATED* please use fetchDepositWithdrawFees instead
        see https://documenter.getpostman.com/view/10287440/SzYXWKPi#4190035d-24b1-453d-833b-37e0a52f88e2
        :param [str]|None codes: list of unified currency codes
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a list of `transaction fees structures <https://docs.ccxt.com/en/latest/manual.html#fees-structure>`
        """
        self.load_markets()
        cryptoList = self.publicGetPaymentsProvidersCryptoList(params)
        result = {}
        cryptoListKeys = list(cryptoList.keys())
        for i in range(0, len(cryptoListKeys)):
            code = cryptoListKeys[i]
            if codes is not None and (not self.in_array(code, codes)):
                continue
            result[code] = {'deposit': None, 'withdraw': None}
            currency = self.currency(code)
            currencyId = self.safe_string(currency, 'id')
            providers = self.safe_value(cryptoList, currencyId, [])
            for j in range(0, len(providers)):
                provider = providers[j]
                type = self.safe_string(provider, 'type')
                commissionDesc = self.safe_string(provider, 'commission_desc')
                fee = self.parse_fixed_float_value(commissionDesc)
                result[code][type] = fee
            result[code]['info'] = providers
        self.options['transactionFees'] = result
        return result

    def fetch_deposit_withdraw_fees(self, codes=None, params={}):
        """
        fetch deposit and withdraw fees
        see https://documenter.getpostman.com/view/10287440/SzYXWKPi#4190035d-24b1-453d-833b-37e0a52f88e2
        :param [str]|None codes: list of unified currency codes
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a list of `transaction fees structures <https://docs.ccxt.com/en/latest/manual.html#fees-structure>`
        """
        self.load_markets()
        response = self.publicGetPaymentsProvidersCryptoList(params)
        result = self.parse_deposit_withdraw_fees(response, codes)
        self.options['transactionFees'] = result
        return result

    def parse_deposit_withdraw_fee(self, fee, currency=None):
        result = self.deposit_withdraw_fee(fee)
        for i in range(0, len(fee)):
            provider = fee[i]
            type = self.safe_string(provider, 'type')
            networkId = self.safe_string(provider, 'name')
            networkCode = self.network_id_to_code(networkId, self.safe_string(currency, 'code'))
            commissionDesc = self.safe_string(provider, 'commission_desc')
            splitCommissionDesc = []
            percentage = None
            if commissionDesc is not None:
                splitCommissionDesc = commissionDesc.split('%')
                splitCommissionDescLength = len(splitCommissionDesc)
                percentage = splitCommissionDescLength >= 2
            network = self.safe_value(result['networks'], networkCode)
            if network is None:
                result['networks'][networkCode] = {'withdraw': {'fee': None, 'percentage': None}, 'deposit': {'fee': None, 'percentage': None}}
            result['networks'][networkCode][type] = {'fee': self.parse_fixed_float_value(self.safe_string(splitCommissionDesc, 0)), 'percentage': percentage}
        return self.assign_default_deposit_withdraw_fees(result)

    def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: an associative dictionary of currencies
        """
        currencyList = self.publicGetCurrencyListExtended(params)
        cryptoList = self.publicGetPaymentsProvidersCryptoList(params)
        result = {}
        for i in range(0, len(currencyList)):
            currency = currencyList[i]
            currencyId = self.safe_string(currency, 'name')
            name = self.safe_string(currency, 'description')
            providers = self.safe_value(cryptoList, currencyId)
            active = False
            type = 'crypto'
            limits = {'deposit': {'min': None, 'max': None}, 'withdraw': {'min': None, 'max': None}}
            fee = None
            depositEnabled = None
            withdrawEnabled = None
            if providers is None:
                active = True
                type = 'fiat'
            else:
                for j in range(0, len(providers)):
                    provider = providers[j]
                    type = self.safe_string(provider, 'type')
                    minValue = self.safe_number(provider, 'min')
                    maxValue = self.safe_number(provider, 'max')
                    if maxValue == 0.0:
                        maxValue = None
                    activeProvider = self.safe_value(provider, 'enabled')
                    if type == 'deposit':
                        if activeProvider and (not depositEnabled):
                            depositEnabled = True
                        elif not activeProvider:
                            depositEnabled = False
                    elif type == 'withdraw':
                        if activeProvider and (not withdrawEnabled):
                            withdrawEnabled = True
                        elif not activeProvider:
                            withdrawEnabled = False
                    if activeProvider:
                        active = True
                        if limits[type]['min'] is None or minValue < limits[type]['min']:
                            limits[type]['min'] = minValue
                            limits[type]['max'] = maxValue
                            if type == 'withdraw':
                                commissionDesc = self.safe_string(provider, 'commission_desc')
                                fee = self.parse_fixed_float_value(commissionDesc)
            code = self.safe_currency_code(currencyId)
            result[code] = {'id': currencyId, 'code': code, 'name': name, 'type': type, 'active': active, 'deposit': depositEnabled, 'withdraw': withdrawEnabled, 'fee': fee, 'precision': self.parse_number('1e-8'), 'limits': limits, 'info': providers}
        return result

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for exmo
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.publicGetPairSettings(params)
        keys = list(response.keys())
        result = []
        for i in range(0, len(keys)):
            id = keys[i]
            market = response[id]
            symbol = id.replace('_', '/')
            baseId, quoteId = symbol.split('/')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            takerString = self.safe_string(market, 'commission_taker_percent')
            makerString = self.safe_string(market, 'commission_maker_percent')
            result.append({'id': id, 'symbol': symbol, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'type': 'spot', 'spot': True, 'margin': True, 'swap': False, 'future': False, 'option': False, 'active': None, 'contract': False, 'linear': None, 'inverse': None, 'taker': self.parse_number(Precise.string_div(takerString, '100')), 'maker': self.parse_number(Precise.string_div(makerString, '100')), 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.parse_number('1e-8'), 'price': self.parse_number(self.parse_precision(self.safe_string(market, 'price_precision')))}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': self.safe_number(market, 'min_quantity'), 'max': self.safe_number(market, 'max_quantity')}, 'price': {'min': self.safe_number(market, 'min_price'), 'max': self.safe_number(market, 'max_price')}, 'cost': {'min': self.safe_number(market, 'min_amount'), 'max': self.safe_number(market, 'max_amount')}}, 'info': market})
        return result

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id'], 'resolution': self.timeframes[timeframe]}
        options = self.safe_value(self.options, 'fetchOHLCV')
        maxLimit = self.safe_integer(options, 'maxLimit', 3000)
        duration = self.parse_timeframe(timeframe)
        now = self.milliseconds()
        if since is None:
            if limit is None:
                limit = 1000
            if limit > maxLimit:
                limit = maxLimit
            request['from'] = int(now / 1000) - limit * duration - 1
            request['to'] = int(now / 1000)
        else:
            request['from'] = int(since / 1000) - 1
            if limit is None:
                request['to'] = int(now / 1000)
            else:
                if limit > maxLimit:
                    raise BadRequest(self.id + ' fetchOHLCV() will serve ' + str(maxLimit) + ' candles at most')
                to = self.sum(since, limit * duration * 1000)
                request['to'] = int(to / 1000)
        response = self.publicGetCandlesHistory(self.extend(request, params))
        candles = self.safe_value(response, 'candles', [])
        return self.parse_ohlcvs(candles, market, timeframe, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        return [self.safe_integer(ohlcv, 't'), self.safe_number(ohlcv, 'o'), self.safe_number(ohlcv, 'h'), self.safe_number(ohlcv, 'l'), self.safe_number(ohlcv, 'c'), self.safe_number(ohlcv, 'v')]

    def parse_balance(self, response):
        result = {'info': response}
        free = self.safe_value(response, 'balances', {})
        used = self.safe_value(response, 'reserved', {})
        currencyIds = list(free.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            if currencyId in free:
                account['free'] = self.safe_string(free, currencyId)
            if currencyId in used:
                account['used'] = self.safe_string(used, currencyId)
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privatePostUserInfo(params)
        return self.parse_balance(response)

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id']}
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetOrderBook(self.extend(request, params))
        result = self.safe_value(response, market['id'])
        return self.parse_order_book(result, market['symbol'], None, 'bid', 'ask')

    def fetch_order_books(self, symbols=None, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data for multiple markets
        :param [str]|None symbols: list of unified market symbols, all symbols fetched if None, default is None
        :param int|None limit: max number of entries per orderbook to return, default is None
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbol
        """
        self.load_markets()
        ids = None
        if symbols is None:
            ids = ','.join(self.ids)
            if len(ids) > 2048:
                numIds = len(self.ids)
                raise ExchangeError(self.id + ' fetchOrderBooks() has ' + str(numIds) + ' symbols exceeding max URL length, you are required to specify a list of symbols in the first argument to fetchOrderBooks')
        else:
            ids = self.market_ids(symbols)
            ids = ','.join(ids)
        request = {'pair': ids}
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetOrderBook(self.extend(request, params))
        result = {}
        marketIds = list(response.keys())
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            symbol = self.safe_symbol(marketId)
            result[symbol] = self.parse_order_book(response[marketId], symbol, None, 'bid', 'ask')
        return result

    def parse_ticker(self, ticker, market=None):
        timestamp = self.safe_timestamp(ticker, 'updated')
        market = self.safe_market(None, market)
        last = self.safe_string(ticker, 'last_trade')
        return self.safe_ticker({'symbol': market['symbol'], 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'high': self.safe_string(ticker, 'high'), 'low': self.safe_string(ticker, 'low'), 'bid': self.safe_string(ticker, 'buy_price'), 'bidVolume': None, 'ask': self.safe_string(ticker, 'sell_price'), 'askVolume': None, 'vwap': None, 'open': None, 'close': last, 'last': last, 'previousClose': None, 'change': None, 'percentage': None, 'average': self.safe_string(ticker, 'avg'), 'baseVolume': self.safe_string(ticker, 'vol'), 'quoteVolume': self.safe_string(ticker, 'vol_curr'), 'info': ticker}, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        response = self.publicGetTicker(params)
        result = {}
        marketIds = list(response.keys())
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            market = self.safe_market(marketId, None, '_')
            symbol = market['symbol']
            ticker = self.safe_value(response, marketId)
            result[symbol] = self.parse_ticker(ticker, market)
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        response = self.publicGetTicker(params)
        market = self.market(symbol)
        return self.parse_ticker(response[market['id']], market)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'date')
        id = self.safe_string(trade, 'trade_id')
        orderId = self.safe_string(trade, 'order_id')
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'quantity')
        costString = self.safe_string(trade, 'amount')
        side = self.safe_string(trade, 'type')
        type = None
        marketId = self.safe_string(trade, 'pair')
        market = self.safe_market(marketId, market, '_')
        symbol = market['symbol']
        takerOrMaker = self.safe_string(trade, 'exec_type')
        fee = None
        feeCostString = self.safe_string(trade, 'commission_amount')
        if feeCostString is not None:
            feeCurrencyId = self.safe_string(trade, 'commission_currency')
            feeCurrencyCode = self.safe_currency_code(feeCurrencyId)
            feeRateString = self.safe_string(trade, 'commission_percent')
            if feeRateString is not None:
                feeRateString = Precise.string_div(feeRateString, '1000', 18)
            fee = {'cost': feeCostString, 'currency': feeCurrencyCode, 'rate': feeRateString}
        return self.safe_trade({'id': id, 'info': trade, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': symbol, 'order': orderId, 'type': type, 'side': side, 'takerOrMaker': takerOrMaker, 'price': priceString, 'amount': amountString, 'cost': costString, 'fee': fee}, market)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id']}
        response = self.publicGetTrades(self.extend(request, params))
        data = self.safe_value(response, market['id'], [])
        return self.parse_trades(data, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument(a single symbol or an array)')
        self.load_markets()
        pair = None
        market = None
        if isinstance(symbol, list):
            numSymbols = len(symbol)
            if numSymbols < 1:
                raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a non-empty symbol array')
            marketIds = self.market_ids(symbol)
            pair = ','.join(marketIds)
        else:
            market = self.market(symbol)
            pair = market['id']
        request = {'pair': pair}
        if limit is not None:
            request['limit'] = limit
        response = self.privatePostUserTrades(self.extend(request, params))
        result = []
        marketIds = list(response.keys())
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            resultMarket = self.safe_market(marketId, None, '_')
            items = response[marketId]
            trades = self.parse_trades(items, resultMarket, since, limit)
            result = self.array_concat(result, trades)
        return self.filter_by_since_limit(result, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        prefix = type + '_' if type == 'market' else ''
        orderType = prefix + side
        orderPrice = price
        if type == 'market' and price is None:
            orderPrice = 0
        request = {'pair': market['id'], 'quantity': self.amount_to_precision(market['symbol'], amount), 'type': orderType, 'price': self.price_to_precision(market['symbol'], orderPrice)}
        method = 'privatePostOrderCreate'
        clientOrderId = self.safe_value_2(params, 'client_id', 'clientOrderId')
        if clientOrderId is not None:
            clientOrderId = self.safe_integer_2(params, 'client_id', 'clientOrderId')
            if clientOrderId is None:
                raise BadRequest(self.id + ' createOrder() client order id must be an integer / numeric literal')
            else:
                request['client_id'] = clientOrderId
            params = self.omit(params, ['client_id', 'clientOrderId'])
        if type == 'stop' or type == 'stop_limit' or type == 'trailing_stop':
            stopPrice = self.safe_number_2(params, 'stop_price', 'stopPrice')
            if stopPrice is None:
                raise InvalidOrder(self.id + ' createOrder() requires a stopPrice extra param for a ' + type + ' order')
            else:
                params = self.omit(params, ['stopPrice', 'stop_price'])
                request['stop_price'] = self.price_to_precision(symbol, stopPrice)
                method = 'privatePostMarginUserOrderCreate'
        response = getattr(self, method)(self.extend(request, params))
        id = self.safe_string(response, 'order_id')
        timestamp = self.milliseconds()
        status = 'open'
        return {'id': id, 'info': response, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'lastTradeTimestamp': None, 'status': status, 'symbol': market['symbol'], 'type': type, 'side': side, 'price': price, 'cost': None, 'amount': amount, 'remaining': amount, 'filled': 0.0, 'fee': None, 'trades': None, 'clientOrderId': clientOrderId, 'average': None}

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: not used by exmo cancelOrder()
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {'order_id': id}
        return self.privatePostOrderCancel(self.extend(request, params))

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: not used by exmo fetchOrder
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {'order_id': str(id)}
        response = self.privatePostOrderTrades(self.extend(request, params))
        order = self.parse_order(response)
        return self.extend(order, {'id': str(id)})

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        """
        fetch all the trades made from a single order
        :param str id: order id
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades to retrieve
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request = {'order_id': str(id)}
        response = self.privatePostOrderTrades(self.extend(request, params))
        trades = self.safe_value(response, 'trades')
        return self.parse_trades(trades, market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
            symbol = market['symbol']
        response = self.privatePostUserOpenOrders(params)
        marketIds = list(response.keys())
        orders = []
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            market = self.safe_market(marketId)
            parsedOrders = self.parse_orders(response[marketId], market)
            orders = self.array_concat(orders, parsedOrders)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'order_id')
        timestamp = self.safe_timestamp(order, 'created')
        symbol = None
        side = self.safe_string(order, 'type')
        marketId = None
        if 'pair' in order:
            marketId = order['pair']
        elif 'in_currency' in order and 'out_currency' in order:
            if side == 'buy':
                marketId = order['in_currency'] + '_' + order['out_currency']
            else:
                marketId = order['out_currency'] + '_' + order['in_currency']
        market = self.safe_market(marketId, market)
        amount = self.safe_number(order, 'quantity')
        if amount is None:
            amountField = 'in_amount' if side == 'buy' else 'out_amount'
            amount = self.safe_number(order, amountField)
        price = self.safe_number(order, 'price')
        cost = self.safe_number(order, 'amount')
        filled = 0.0
        trades = []
        transactions = self.safe_value(order, 'trades', [])
        feeCost = None
        lastTradeTimestamp = None
        average = None
        numTransactions = len(transactions)
        if numTransactions > 0:
            feeCost = 0
            for i in range(0, numTransactions):
                trade = self.parse_trade(transactions[i], market)
                if id is None:
                    id = trade['order']
                if timestamp is None:
                    timestamp = trade['timestamp']
                if timestamp > trade['timestamp']:
                    timestamp = trade['timestamp']
                filled = self.sum(filled, trade['amount'])
                feeCost = self.sum(feeCost, trade['fee']['cost'])
                trades.append(trade)
            lastTradeTimestamp = trades[numTransactions - 1]['timestamp']
        status = self.safe_string(order, 'status')
        remaining = None
        if amount is not None:
            remaining = amount - filled
            if filled >= amount:
                status = 'closed'
            else:
                status = 'open'
        if market is None:
            market = self.get_market_from_trades(trades)
        feeCurrency = None
        if market is not None:
            symbol = market['symbol']
            feeCurrency = market['quote']
        if cost is None:
            if price is not None:
                cost = price * filled
        elif filled > 0:
            if average is None:
                average = cost / filled
            if price is None:
                price = cost / filled
        fee = {'cost': feeCost, 'currency': feeCurrency}
        clientOrderId = self.safe_integer(order, 'client_id')
        return {'id': id, 'clientOrderId': clientOrderId, 'datetime': self.iso8601(timestamp), 'timestamp': timestamp, 'lastTradeTimestamp': lastTradeTimestamp, 'status': status, 'symbol': symbol, 'type': 'limit', 'timeInForce': None, 'postOnly': None, 'side': side, 'price': price, 'stopPrice': None, 'cost': cost, 'amount': amount, 'filled': filled, 'remaining': remaining, 'average': average, 'trades': trades, 'fee': fee, 'info': order}

    def fetch_canceled_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple canceled orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: timestamp in ms of the earliest order, default is None
        :param int|None limit: max number of orders to return, default is None
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        if since is not None:
            request['offset'] = limit
        if limit is not None:
            request['limit'] = limit
        market = None
        if symbol is not None:
            market = self.market(symbol)
        response = self.privatePostUserCancelledOrders(self.extend(request, params))
        return self.parse_orders(response, market, since, limit, params)

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        response = self.privatePostDepositAddress(params)
        depositAddress = self.safe_string(response, code)
        address = None
        tag = None
        if depositAddress:
            addressAndTag = depositAddress.split(',')
            address = addressAndTag[0]
            numParts = len(addressAndTag)
            if numParts > 1:
                tag = addressAndTag[1]
        self.check_address(address)
        return {'currency': code, 'address': address, 'tag': tag, 'network': None, 'info': response}

    def get_market_from_trades(self, trades):
        tradesBySymbol = self.index_by(trades, 'pair')
        symbols = list(tradesBySymbol.keys())
        numSymbols = len(symbols)
        if numSymbols == 1:
            return self.markets[symbols[0]]
        return None

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.load_markets()
        currency = self.currency(code)
        request = {'amount': amount, 'currency': currency['id'], 'address': address}
        if tag is not None:
            request['invoice'] = tag
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper(params, 'network')
        network = self.safe_string(networks, network, network)
        if network is not None:
            request['transport'] = network
            params = self.omit(params, 'network')
        response = self.privatePostWithdrawCrypt(self.extend(request, params))
        return self.parse_transaction(response, currency)

    def parse_transaction_status(self, status):
        statuses = {'transferred': 'ok', 'paid': 'ok', 'pending': 'pending', 'processing': 'pending', 'verifying': 'pending'}
        return self.safe_string(statuses, status, status)

    def parse_transaction(self, transaction, currency=None):
        id = self.safe_string_2(transaction, 'order_id', 'task_id')
        timestamp = self.safe_timestamp_2(transaction, 'dt', 'created')
        updated = self.safe_timestamp(transaction, 'updated')
        amount = self.safe_string(transaction, 'amount')
        if amount is not None:
            amount = Precise.string_abs(amount)
        status = self.parse_transaction_status(self.safe_string_lower(transaction, 'status'))
        txid = self.safe_string(transaction, 'txid')
        if txid is None:
            extra = self.safe_value(transaction, 'extra', {})
            extraTxid = self.safe_string(extra, 'txid')
            if extraTxid != '':
                txid = extraTxid
        type = self.safe_string(transaction, 'type')
        currencyId = self.safe_string_2(transaction, 'curr', 'currency')
        code = self.safe_currency_code(currencyId, currency)
        address = None
        tag = None
        comment = None
        account = self.safe_string(transaction, 'account')
        if type == 'deposit':
            comment = account
        elif type == 'withdrawal':
            address = account
            if address is not None:
                parts = address.split(':')
                numParts = len(parts)
                if numParts == 2:
                    address = self.safe_string(parts, 1)
                    address = address.replace(' ', '')
        fee = None
        if not self.fees['transaction']['percentage']:
            key = 'withdraw' if type == 'withdrawal' else 'deposit'
            feeCost = self.safe_string(transaction, 'commission')
            if feeCost is None:
                transactionFees = self.safe_value(self.options, 'transactionFees', {})
                codeFees = self.safe_value(transactionFees, code, {})
                feeCost = self.safe_string(codeFees, key)
            provider = self.safe_string(transaction, 'provider')
            if provider == 'cashback':
                feeCost = '0'
            if feeCost is not None:
                if type == 'withdrawal':
                    amount = Precise.string_sub(amount, feeCost)
                fee = {'cost': self.parse_number(feeCost), 'currency': code, 'rate': None}
        network = self.safe_string(transaction, 'provider')
        return {'info': transaction, 'id': id, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'currency': code, 'amount': amount, 'network': network, 'address': address, 'addressTo': address, 'addressFrom': None, 'tag': tag, 'tagTo': tag, 'tagFrom': None, 'status': status, 'type': type, 'updated': updated, 'comment': comment, 'txid': txid, 'fee': fee}

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        """
        fetch history of deposits and withdrawals
        :param str|None code: unified currency code for the currency of the transactions, default is None
        :param int|None since: timestamp in ms of the earliest transaction, default is None
        :param int|None limit: max number of transactions to return, default is None
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a list of `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        if since is not None:
            request['date'] = int(since / 1000)
        currency = None
        if code is not None:
            currency = self.currency(code)
        response = self.privatePostWalletHistory(self.extend(request, params))
        return self.parse_transactions(response['history'], currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        currency = None
        request = {'type': 'withdraw'}
        if limit is not None:
            request['limit'] = limit
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.privatePostWalletOperations(self.extend(request, params))
        items = self.safe_value(response, 'items', [])
        return self.parse_transactions(items, currency, since, limit)

    def fetch_withdrawal(self, id, code=None, params={}):
        """
        fetch data on a currency withdrawal via the withdrawal id
        :param str id: withdrawal id
        :param str|None code: unified currency code of the currency withdrawn, default is None
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        currency = None
        request = {'order_id': id, 'type': 'withdraw'}
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.privatePostWalletOperations(self.extend(request, params))
        items = self.safe_value(response, 'items', [])
        first = self.safe_value(items, 0, {})
        return self.parse_transaction(first, currency)

    def fetch_deposit(self, id=None, code=None, params={}):
        """
        fetch information on a deposit
        :param str id: deposit id
        :param str|None code: unified currency code, default is None
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        currency = None
        request = {'order_id': id, 'type': 'deposit'}
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.privatePostWalletOperations(self.extend(request, params))
        items = self.safe_value(response, 'items', [])
        first = self.safe_value(items, 0, {})
        return self.parse_transaction(first, currency)

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the exmo api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        currency = None
        request = {'type': 'deposit'}
        if limit is not None:
            request['limit'] = limit
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.privatePostWalletOperations(self.extend(request, params))
        items = self.safe_value(response, 'items', [])
        return self.parse_transactions(items, currency, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        if api != 'web':
            url += self.version + '/'
        url += path
        if api == 'public' or api == 'web':
            if params:
                url += '?' + self.urlencode(params)
        elif api == 'private':
            self.check_required_credentials()
            nonce = self.nonce()
            body = self.urlencode(self.extend({'nonce': nonce}, params))
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Key': self.apiKey, 'Sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512)}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def nonce(self):
        return self.milliseconds()

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if 'result' in response or 'errmsg' in response:
            success = self.safe_value(response, 'result', False)
            if isinstance(success, str):
                if success == 'true' or success == '1':
                    success = True
                else:
                    success = False
            if not success:
                code = None
                message = self.safe_string_2(response, 'error', 'errmsg')
                errorParts = message.split(':')
                numParts = len(errorParts)
                if numParts > 1:
                    errorSubParts = errorParts[0].split(' ')
                    numSubParts = len(errorSubParts)
                    code = errorSubParts[1] if numSubParts > 1 else errorSubParts[0]
                feedback = self.id + ' ' + body
                self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
                self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
                raise ExchangeError(feedback)