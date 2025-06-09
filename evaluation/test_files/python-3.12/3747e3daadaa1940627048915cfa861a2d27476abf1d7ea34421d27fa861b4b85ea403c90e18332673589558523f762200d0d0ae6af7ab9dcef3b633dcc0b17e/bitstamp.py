from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import OnMaintenance
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise

class bitstamp(Exchange):

    def describe(self):
        return self.deep_extend(super(bitstamp, self).describe(), {'id': 'bitstamp', 'name': 'Bitstamp', 'countries': ['GB'], 'rateLimit': 75, 'version': 'v2', 'userAgent': self.userAgents['chrome'], 'pro': True, 'has': {'CORS': True, 'spot': True, 'margin': False, 'swap': False, 'future': False, 'option': False, 'addMargin': False, 'cancelAllOrders': True, 'cancelOrder': True, 'createOrder': True, 'createReduceOnlyOrder': False, 'createStopLimitOrder': False, 'createStopMarketOrder': False, 'createStopOrder': False, 'fetchBalance': True, 'fetchBorrowRate': False, 'fetchBorrowRateHistories': False, 'fetchBorrowRateHistory': False, 'fetchBorrowRates': False, 'fetchBorrowRatesPerSymbol': False, 'fetchCurrencies': True, 'fetchDepositAddress': True, 'fetchFundingHistory': False, 'fetchFundingRate': False, 'fetchFundingRateHistory': False, 'fetchFundingRates': False, 'fetchIndexOHLCV': False, 'fetchLedger': True, 'fetchLeverage': False, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMarkOHLCV': False, 'fetchMyTrades': True, 'fetchOHLCV': True, 'fetchOpenInterestHistory': False, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchPosition': False, 'fetchPositionMode': False, 'fetchPositions': False, 'fetchPositionsRisk': False, 'fetchPremiumIndexOHLCV': False, 'fetchTicker': True, 'fetchTrades': True, 'fetchTradingFee': True, 'fetchTradingFees': True, 'fetchTransactionFees': True, 'fetchTransactions': True, 'fetchWithdrawals': True, 'reduceMargin': False, 'setLeverage': False, 'setMarginMode': False, 'setPositionMode': False, 'withdraw': True}, 'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/27786377-8c8ab57e-5fe9-11e7-8ea4-2b05b6bcceec.jpg', 'api': {'public': 'https://www.bitstamp.net/api', 'private': 'https://www.bitstamp.net/api'}, 'www': 'https://www.bitstamp.net', 'doc': 'https://www.bitstamp.net/api'}, 'timeframes': {'1m': '60', '3m': '180', '5m': '300', '15m': '900', '30m': '1800', '1h': '3600', '2h': '7200', '4h': '14400', '6h': '21600', '12h': '43200', '1d': '86400', '1w': '259200'}, 'requiredCredentials': {'apiKey': True, 'secret': True}, 'api': {'public': {'get': {'ohlc/{pair}/': 1, 'order_book/{pair}/': 1, 'ticker_hour/{pair}/': 1, 'ticker/{pair}/': 1, 'transactions/{pair}/': 1, 'trading-pairs-info/': 1}}, 'private': {'post': {'balance/': 1, 'balance/{pair}/': 1, 'bch_withdrawal/': 1, 'bch_address/': 1, 'user_transactions/': 1, 'user_transactions/{pair}/': 1, 'open_orders/all/': 1, 'open_orders/{pair}/': 1, 'order_status/': 1, 'cancel_order/': 1, 'cancel_all_orders/': 1, 'cancel_all_orders/{pair}/': 1, 'buy/{pair}/': 1, 'buy/market/{pair}/': 1, 'buy/instant/{pair}/': 1, 'sell/{pair}/': 1, 'sell/market/{pair}/': 1, 'sell/instant/{pair}/': 1, 'transfer-to-main/': 1, 'transfer-from-main/': 1, 'withdrawal-requests/': 1, 'withdrawal/open/': 1, 'withdrawal/status/': 1, 'withdrawal/cancel/': 1, 'liquidation_address/new/': 1, 'liquidation_address/info/': 1, 'btc_unconfirmed/': 1, 'websockets_token/': 1, 'btc_withdrawal/': 1, 'btc_address/': 1, 'ripple_withdrawal/': 1, 'ripple_address/': 1, 'ltc_withdrawal/': 1, 'ltc_address/': 1, 'eth_withdrawal/': 1, 'eth_address/': 1, 'xrp_withdrawal/': 1, 'xrp_address/': 1, 'xlm_withdrawal/': 1, 'xlm_address/': 1, 'pax_withdrawal/': 1, 'pax_address/': 1, 'link_withdrawal/': 1, 'link_address/': 1, 'usdc_withdrawal/': 1, 'usdc_address/': 1, 'omg_withdrawal/': 1, 'omg_address/': 1, 'dai_withdrawal/': 1, 'dai_address/': 1, 'knc_withdrawal/': 1, 'knc_address/': 1, 'mkr_withdrawal/': 1, 'mkr_address/': 1, 'zrx_withdrawal/': 1, 'zrx_address/': 1, 'gusd_withdrawal/': 1, 'gusd_address/': 1, 'aave_withdrawal/': 1, 'aave_address/': 1, 'bat_withdrawal/': 1, 'bat_address/': 1, 'uma_withdrawal/': 1, 'uma_address/': 1, 'snx_withdrawal/': 1, 'snx_address/': 1, 'uni_withdrawal/': 1, 'uni_address/': 1, 'yfi_withdrawal/': 1, 'yfi_address': 1, 'audio_withdrawal/': 1, 'audio_address/': 1, 'crv_withdrawal/': 1, 'crv_address/': 1, 'algo_withdrawal/': 1, 'algo_address/': 1, 'comp_withdrawal/': 1, 'comp_address/': 1, 'grt_withdrawal': 1, 'grt_address/': 1, 'usdt_withdrawal/': 1, 'usdt_address/': 1, 'eurt_withdrawal/': 1, 'eurt_address/': 1, 'matic_withdrawal/': 1, 'matic_address/': 1, 'sushi_withdrawal/': 1, 'sushi_address/': 1, 'chz_withdrawal/': 1, 'chz_address/': 1, 'enj_withdrawal/': 1, 'enj_address/': 1, 'alpha_withdrawal/': 1, 'alpha_address/': 1, 'ftt_withdrawal/': 1, 'ftt_address/': 1, 'storj_withdrawal/': 1, 'storj_address/': 1, 'axs_withdrawal/': 1, 'axs_address/': 1, 'sand_withdrawal/': 1, 'sand_address/': 1, 'hbar_withdrawal/': 1, 'hbar_address/': 1, 'rgt_withdrawal/': 1, 'rgt_address/': 1, 'fet_withdrawal/': 1, 'fet_address/': 1, 'skl_withdrawal/': 1, 'skl_address/': 1, 'cel_withdrawal/': 1, 'cel_address/': 1, 'sxp_withdrawal/': 1, 'sxp_address/': 1, 'ada_withdrawal/': 1, 'ada_address/': 1, 'slp_withdrawal/': 1, 'slp_address/': 1, 'ftm_withdrawal/': 1, 'ftm_address/': 1, 'perp_withdrawal/': 1, 'perp_address/': 1, 'dydx_withdrawal/': 1, 'dydx_address/': 1, 'gala_withdrawal/': 1, 'gala_address/': 1, 'shib_withdrawal/': 1, 'shib_address/': 1, 'amp_withdrawal/': 1, 'amp_address/': 1, 'sgb_withdrawal/': 1, 'sgb_address/': 1, 'avax_withdrawal/': 1, 'avax_address/': 1, 'wbtc_withdrawal/': 1, 'wbtc_address/': 1, 'ctsi_withdrawal/': 1, 'ctsi_address/': 1, 'cvx_withdrawal/': 1, 'cvx_address/': 1, 'imx_withdrawal/': 1, 'imx_address/': 1, 'nexo_withdrawal/': 1, 'nexo_address/': 1, 'ust_withdrawal/': 1, 'ust_address/': 1, 'ant_withdrawal/': 1, 'ant_address/': 1, 'gods_withdrawal/': 1, 'gods_address/': 1, 'rad_withdrawal/': 1, 'rad_address/': 1, 'band_withdrawal/': 1, 'band_address/': 1, 'inj_withdrawal/': 1, 'inj_address/': 1, 'rly_withdrawal/': 1, 'rly_address/': 1, 'rndr_withdrawal/': 1, 'rndr_address/': 1, 'vega_withdrawal/': 1, 'vega_address/': 1, '1inch_withdrawal/': 1, '1inch_address/': 1, 'ens_withdrawal/': 1, 'ens_address/': 1, 'mana_withdrawal/': 1, 'mana_address/': 1, 'lrc_withdrawal/': 1, 'lrc_address/': 1, 'ape_withdrawal/': 1, 'ape_address/': 1, 'mpl_withdrawal/': 1, 'mpl_address/': 1, 'euroc_withdrawal/': 1, 'euroc_address/': 1}}}, 'fees': {'trading': {'tierBased': True, 'percentage': True, 'taker': self.parse_number('0.005'), 'maker': self.parse_number('0.005'), 'tiers': {'taker': [[self.parse_number('0'), self.parse_number('0.005')], [self.parse_number('20000'), self.parse_number('0.0025')], [self.parse_number('100000'), self.parse_number('0.0024')], [self.parse_number('200000'), self.parse_number('0.0022')], [self.parse_number('400000'), self.parse_number('0.0020')], [self.parse_number('600000'), self.parse_number('0.0015')], [self.parse_number('1000000'), self.parse_number('0.0014')], [self.parse_number('2000000'), self.parse_number('0.0013')], [self.parse_number('4000000'), self.parse_number('0.0012')], [self.parse_number('20000000'), self.parse_number('0.0011')], [self.parse_number('50000000'), self.parse_number('0.0010')], [self.parse_number('100000000'), self.parse_number('0.0007')], [self.parse_number('500000000'), self.parse_number('0.0005')], [self.parse_number('2000000000'), self.parse_number('0.0003')], [self.parse_number('6000000000'), self.parse_number('0.0001')], [self.parse_number('20000000000'), self.parse_number('0.00005')], [self.parse_number('20000000001'), self.parse_number('0')]], 'maker': [[self.parse_number('0'), self.parse_number('0.005')], [self.parse_number('20000'), self.parse_number('0.0025')], [self.parse_number('100000'), self.parse_number('0.0024')], [self.parse_number('200000'), self.parse_number('0.0022')], [self.parse_number('400000'), self.parse_number('0.0020')], [self.parse_number('600000'), self.parse_number('0.0015')], [self.parse_number('1000000'), self.parse_number('0.0014')], [self.parse_number('2000000'), self.parse_number('0.0013')], [self.parse_number('4000000'), self.parse_number('0.0012')], [self.parse_number('20000000'), self.parse_number('0.0011')], [self.parse_number('50000000'), self.parse_number('0.0010')], [self.parse_number('100000000'), self.parse_number('0.0007')], [self.parse_number('500000000'), self.parse_number('0.0005')], [self.parse_number('2000000000'), self.parse_number('0.0003')], [self.parse_number('6000000000'), self.parse_number('0.0001')], [self.parse_number('20000000000'), self.parse_number('0.00005')], [self.parse_number('20000000001'), self.parse_number('0')]]}}, 'funding': {'tierBased': False, 'percentage': False, 'withdraw': {}, 'deposit': {'BTC': 0, 'BCH': 0, 'LTC': 0, 'ETH': 0, 'XRP': 0, 'XLM': 0, 'PAX': 0, 'USD': 7.5, 'EUR': 0}}}, 'precisionMode': TICK_SIZE, 'commonCurrencies': {'UST': 'USTC'}, 'exceptions': {'exact': {'No permission found': PermissionDenied, 'API key not found': AuthenticationError, 'IP address not allowed': PermissionDenied, 'Invalid nonce': InvalidNonce, 'Invalid signature': AuthenticationError, 'Authentication failed': AuthenticationError, 'Missing key, signature and nonce parameters': AuthenticationError, 'Wrong API key format': AuthenticationError, 'Your account is frozen': PermissionDenied, 'Please update your profile with your FATCA information, before using API.': PermissionDenied, 'Order not found': OrderNotFound, 'Price is more than 20% below market price.': InvalidOrder, "Bitstamp.net is under scheduled maintenance. We'll be back soon.": OnMaintenance, 'Order could not be placed.': ExchangeNotAvailable, 'Invalid offset.': BadRequest}, 'broad': {'Minimum order size is': InvalidOrder, 'Check your account balance for details.': InsufficientFunds, 'Ensure self value has at least': InvalidAddress}}})

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for bitstamp
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.fetch_markets_from_cache(params)
        result = []
        for i in range(0, len(response)):
            market = response[i]
            name = self.safe_string(market, 'name')
            base, quote = name.split('/')
            baseId = base.lower()
            quoteId = quote.lower()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            minimumOrder = self.safe_string(market, 'minimum_order')
            parts = minimumOrder.split(' ')
            status = self.safe_string(market, 'trading')
            result.append({'id': self.safe_string(market, 'url_symbol'), 'marketId': baseId + '_' + quoteId, 'symbol': base + '/' + quote, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'type': 'spot', 'spot': True, 'margin': False, 'future': False, 'swap': False, 'option': False, 'active': status == 'Enabled', 'contract': False, 'linear': None, 'inverse': None, 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.parse_number(self.parse_precision(self.safe_string(market, 'base_decimals'))), 'price': self.parse_number(self.parse_precision(self.safe_string(market, 'counter_decimals')))}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': None, 'max': None}, 'price': {'min': None, 'max': None}, 'cost': {'min': self.safe_number(parts, 0), 'max': None}}, 'info': market})
        return result

    def construct_currency_object(self, id, code, name, precision, minCost, originalPayload):
        currencyType = 'crypto'
        description = self.describe()
        if self.is_fiat(code):
            currencyType = 'fiat'
        tickSize = self.parse_number(self.parse_precision(self.number_to_string(precision)))
        return {'id': id, 'code': code, 'info': originalPayload, 'type': currencyType, 'name': name, 'active': True, 'deposit': None, 'withdraw': None, 'fee': self.safe_number(description['fees']['funding']['withdraw'], code), 'precision': tickSize, 'limits': {'amount': {'min': tickSize, 'max': None}, 'price': {'min': tickSize, 'max': None}, 'cost': {'min': minCost, 'max': None}, 'withdraw': {'min': None, 'max': None}}}

    def fetch_markets_from_cache(self, params={}):
        options = self.safe_value(self.options, 'fetchMarkets', {})
        timestamp = self.safe_integer(options, 'timestamp')
        expires = self.safe_integer(options, 'expires', 1000)
        now = self.milliseconds()
        if timestamp is None or now - timestamp > expires:
            response = self.publicGetTradingPairsInfo(params)
            self.options['fetchMarkets'] = self.extend(options, {'response': response, 'timestamp': now})
        return self.safe_value(self.options['fetchMarkets'], 'response')

    def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = self.fetch_markets_from_cache(params)
        result = {}
        for i in range(0, len(response)):
            market = response[i]
            name = self.safe_string(market, 'name')
            base, quote = name.split('/')
            baseId = base.lower()
            quoteId = quote.lower()
            base = self.safe_currency_code(base)
            quote = self.safe_currency_code(quote)
            description = self.safe_string(market, 'description')
            baseDescription, quoteDescription = description.split(' / ')
            minimumOrder = self.safe_string(market, 'minimum_order')
            parts = minimumOrder.split(' ')
            cost = parts[0]
            if not base in result:
                baseDecimals = self.safe_integer(market, 'base_decimals')
                result[base] = self.construct_currency_object(baseId, base, baseDescription, baseDecimals, None, market)
            if not quote in result:
                counterDecimals = self.safe_integer(market, 'counter_decimals')
                result[quote] = self.construct_currency_object(quoteId, quote, quoteDescription, counterDecimals, self.parse_number(cost), market)
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id']}
        response = self.publicGetOrderBookPair(self.extend(request, params))
        microtimestamp = self.safe_integer(response, 'microtimestamp')
        timestamp = int(microtimestamp / 1000)
        orderbook = self.parse_order_book(response, market['symbol'], timestamp)
        orderbook['nonce'] = microtimestamp
        return orderbook

    def parse_ticker(self, ticker, market=None):
        symbol = self.safe_symbol(None, market)
        timestamp = self.safe_timestamp(ticker, 'timestamp')
        vwap = self.safe_string(ticker, 'vwap')
        baseVolume = self.safe_string(ticker, 'volume')
        quoteVolume = Precise.string_mul(baseVolume, vwap)
        last = self.safe_string(ticker, 'last')
        return self.safe_ticker({'symbol': symbol, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'high': self.safe_string(ticker, 'high'), 'low': self.safe_string(ticker, 'low'), 'bid': self.safe_string(ticker, 'bid'), 'bidVolume': None, 'ask': self.safe_string(ticker, 'ask'), 'askVolume': None, 'vwap': vwap, 'open': self.safe_string(ticker, 'open'), 'close': last, 'last': last, 'previousClose': None, 'change': None, 'percentage': None, 'average': None, 'baseVolume': baseVolume, 'quoteVolume': quoteVolume, 'info': ticker}, market)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id']}
        ticker = self.publicGetTickerPair(self.extend(request, params))
        return self.parse_ticker(ticker, market)

    def get_currency_id_from_transaction(self, transaction):
        currencyId = self.safe_string_lower(transaction, 'currency')
        if currencyId is not None:
            return currencyId
        transaction = self.omit(transaction, ['fee', 'price', 'datetime', 'type', 'status', 'id'])
        ids = list(transaction.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            if id.find('_') < 0:
                value = self.safe_number(transaction, id)
                if value is not None and value != 0:
                    return id
        return None

    def get_market_from_trade(self, trade):
        trade = self.omit(trade, ['fee', 'price', 'datetime', 'tid', 'type', 'order_id', 'side'])
        currencyIds = list(trade.keys())
        numCurrencyIds = len(currencyIds)
        if numCurrencyIds > 2:
            raise ExchangeError(self.id + ' getMarketFromTrade() too many keys: ' + self.json(currencyIds) + ' in the trade: ' + self.json(trade))
        if numCurrencyIds == 2:
            marketId = currencyIds[0] + currencyIds[1]
            if marketId in self.markets_by_id:
                return self.markets_by_id[marketId]
            marketId = currencyIds[1] + currencyIds[0]
            if marketId in self.markets_by_id:
                return self.markets_by_id[marketId]
        return None

    def parse_trade(self, trade, market=None):
        id = self.safe_string_2(trade, 'id', 'tid')
        symbol = None
        side = None
        priceString = self.safe_string(trade, 'price')
        amountString = self.safe_string(trade, 'amount')
        orderId = self.safe_string(trade, 'order_id')
        type = None
        costString = self.safe_string(trade, 'cost')
        if market is None:
            keys = list(trade.keys())
            for i in range(0, len(keys)):
                if keys[i].find('_') >= 0:
                    marketId = keys[i].replace('_', '')
                    if marketId in self.markets_by_id:
                        market = self.markets_by_id[marketId]
            if market is None:
                market = self.get_market_from_trade(trade)
        feeCostString = self.safe_string(trade, 'fee')
        feeCurrency = None
        if market is not None:
            priceString = self.safe_string(trade, market['marketId'], priceString)
            amountString = self.safe_string(trade, market['baseId'], amountString)
            costString = self.safe_string(trade, market['quoteId'], costString)
            feeCurrency = market['quote']
            symbol = market['symbol']
        datetimeString = self.safe_string_2(trade, 'date', 'datetime')
        timestamp = None
        if datetimeString is not None:
            if datetimeString.find(' ') >= 0:
                timestamp = self.parse8601(datetimeString)
            else:
                timestamp = int(datetimeString)
                timestamp = timestamp * 1000
        if 'id' in trade:
            if amountString is not None:
                isAmountNeg = Precise.string_lt(amountString, '0')
                if isAmountNeg:
                    side = 'sell'
                    amountString = Precise.string_neg(amountString)
                else:
                    side = 'buy'
        else:
            side = self.safe_string(trade, 'type')
            if side == '1':
                side = 'sell'
            elif side == '0':
                side = 'buy'
            else:
                side = None
        if costString is not None:
            costString = Precise.string_abs(costString)
        fee = None
        if feeCostString is not None:
            fee = {'cost': feeCostString, 'currency': feeCurrency}
        return self.safe_trade({'id': id, 'info': trade, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': symbol, 'order': orderId, 'type': type, 'side': side, 'takerOrMaker': None, 'price': priceString, 'amount': amountString, 'cost': costString, 'fee': fee}, market)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id'], 'time': 'hour'}
        response = self.publicGetTransactionsPair(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        return [self.safe_timestamp(ohlcv, 'timestamp'), self.safe_number(ohlcv, 'open'), self.safe_number(ohlcv, 'high'), self.safe_number(ohlcv, 'low'), self.safe_number(ohlcv, 'close'), self.safe_number(ohlcv, 'volume')]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id'], 'step': self.timeframes[timeframe]}
        duration = self.parse_timeframe(timeframe)
        if limit is None:
            if since is None:
                raise ArgumentsRequired(self.id + ' fetchOHLCV() requires a since argument or a limit argument')
            else:
                limit = 1000
                start = int(since / 1000)
                request['start'] = start
                request['end'] = self.sum(start, limit * duration)
                request['limit'] = limit
        else:
            if since is not None:
                start = int(since / 1000)
                request['start'] = start
                request['end'] = self.sum(start, limit * duration)
            request['limit'] = min(limit, 1000)
        response = self.publicGetOhlcPair(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        ohlc = self.safe_value(data, 'ohlc', [])
        return self.parse_ohlcvs(ohlc, market, timeframe, since, limit)

    def parse_balance(self, response):
        result = {'info': response, 'timestamp': None, 'datetime': None}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            currencyId = currency['id']
            account = self.account()
            account['free'] = self.safe_string(response, currencyId + '_available')
            account['used'] = self.safe_string(response, currencyId + '_reserved')
            account['total'] = self.safe_string(response, currencyId + '_balance')
            result[code] = account
        return self.safe_balance(result)

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        response = self.privatePostBalance(params)
        return self.parse_balance(response)

    def fetch_trading_fee(self, symbol, params={}):
        """
        fetch the trading fees for a market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'pair': market['id']}
        response = self.privatePostBalancePair(self.extend(request, params))
        return self.parse_trading_fee(response, market)

    def parse_trading_fee(self, fee, market=None):
        market = self.safe_market(None, market)
        feeString = self.safe_string(fee, market['id'] + '_fee')
        dividedFeeString = Precise.string_div(feeString, '100')
        tradeFee = self.parse_number(dividedFeeString)
        return {'info': fee, 'symbol': market['symbol'], 'maker': tradeFee, 'taker': tradeFee}

    def parse_trading_fees(self, fees):
        result = {'info': fees}
        symbols = self.symbols
        for i in range(0, len(symbols)):
            symbol = symbols[i]
            market = self.market(symbol)
            fee = self.parse_trading_fee(fees, market)
            result[symbol] = fee
        return result

    def fetch_trading_fees(self, params={}):
        """
        fetch the trading fees for multiple markets
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>` indexed by market symbols
        """
        self.load_markets()
        response = self.privatePostBalance(params)
        return self.parse_trading_fees(response)

    def parse_transaction_fees(self, balance):
        withdraw = {}
        ids = list(balance.keys())
        for i in range(0, len(ids)):
            id = ids[i]
            if id.find('_withdrawal_fee') >= 0:
                currencyId = id.split('_')[0]
                code = self.safe_currency_code(currencyId)
                withdraw[code] = self.safe_number(balance, id)
        return {'info': balance, 'withdraw': withdraw, 'deposit': {}}

    def fetch_transaction_fees(self, codes=None, params={}):
        """
        fetch transaction fees
        :param [str]|None codes: not used by bitstamp fetchTransactionFees()
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [dict]: a list of `fee structures <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        self.load_markets()
        balance = self.privatePostBalance(params)
        return self.parse_transaction_fees(balance)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        method = 'privatePost' + self.capitalize(side)
        request = {'pair': market['id'], 'amount': self.amount_to_precision(symbol, amount)}
        if type == 'market':
            method += 'Market'
        elif type == 'instant':
            method += 'Instant'
        else:
            request['price'] = self.price_to_precision(symbol, price)
        method += 'Pair'
        clientOrderId = self.safe_string_2(params, 'client_order_id', 'clientOrderId')
        if clientOrderId is not None:
            request['client_order_id'] = clientOrderId
            params = self.omit(params, ['client_order_id', 'clientOrderId'])
        response = getattr(self, method)(self.extend(request, params))
        order = self.parse_order(response, market)
        return self.extend(order, {'type': type})

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {'id': id}
        return self.privatePostCancelOrder(self.extend(request, params))

    def cancel_all_orders(self, symbol=None, params={}):
        """
        cancel all open orders
        :param str|None symbol: unified market symbol, only orders in the market of self symbol are cancelled when symbol is not None
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = None
        request = {}
        method = 'privatePostCancelAllOrders'
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
            method = 'privatePostCancelAllOrdersPair'
        return getattr(self, method)(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {'In Queue': 'open', 'Open': 'open', 'Finished': 'closed', 'Canceled': 'canceled'}
        return self.safe_string(statuses, status, status)

    def fetch_order_status(self, id, symbol=None, params={}):
        self.load_markets()
        clientOrderId = self.safe_value_2(params, 'client_order_id', 'clientOrderId')
        request = {}
        if clientOrderId is not None:
            request['client_order_id'] = clientOrderId
            params = self.omit(params, ['client_order_id', 'clientOrderId'])
        else:
            request['id'] = id
        response = self.privatePostOrderStatus(self.extend(request, params))
        return self.parse_order_status(self.safe_string(response, 'status'))

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        clientOrderId = self.safe_value_2(params, 'client_order_id', 'clientOrderId')
        request = {}
        if clientOrderId is not None:
            request['client_order_id'] = clientOrderId
            params = self.omit(params, ['client_order_id', 'clientOrderId'])
        else:
            request['id'] = id
        response = self.privatePostOrderStatus(self.extend(request, params))
        return self.parse_order(response, market)

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        self.load_markets()
        request = {}
        method = 'privatePostUserTransactions'
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
            method += 'Pair'
        if limit is not None:
            request['limit'] = limit
        response = getattr(self, method)(self.extend(request, params))
        result = self.filter_by(response, 'type', '2')
        return self.parse_trades(result, market, since, limit)

    def fetch_transactions(self, code=None, since=None, limit=None, params={}):
        """
        fetch history of deposits and withdrawals
        :param str|None code: unified currency code for the currency of the transactions, default is None
        :param int|None since: timestamp in ms of the earliest transaction, default is None
        :param int|None limit: max number of transactions to return, default is None
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a list of `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        response = self.privatePostUserTransactions(self.extend(request, params))
        currency = None
        if code is not None:
            currency = self.currency(code)
        transactions = self.filter_by_array(response, 'type', ['0', '1'], False)
        return self.parse_transactions(transactions, currency, since, limit)

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        if since is not None:
            request['timedelta'] = self.milliseconds() - since
        else:
            request['timedelta'] = 50000000
        response = self.privatePostWithdrawalRequests(self.extend(request, params))
        return self.parse_transactions(response, None, since, limit)

    def parse_transaction(self, transaction, currency=None):
        timestamp = self.parse8601(self.safe_string(transaction, 'datetime'))
        id = self.safe_string(transaction, 'id')
        currencyId = self.get_currency_id_from_transaction(transaction)
        code = self.safe_currency_code(currencyId, currency)
        feeCost = self.safe_number(transaction, 'fee')
        feeCurrency = None
        amount = None
        if 'amount' in transaction:
            amount = self.safe_number(transaction, 'amount')
        elif currency is not None:
            amount = self.safe_number(transaction, currency['id'], amount)
            feeCurrency = currency['code']
        elif code is not None and currencyId is not None:
            amount = self.safe_number(transaction, currencyId, amount)
            feeCurrency = code
        if amount is not None:
            amount = abs(amount)
        status = 'ok'
        if 'status' in transaction:
            status = self.parse_transaction_status(self.safe_string(transaction, 'status'))
        type = None
        if 'type' in transaction:
            rawType = self.safe_string(transaction, 'type')
            if rawType == '0':
                type = 'deposit'
            elif rawType == '1':
                type = 'withdrawal'
        else:
            type = 'withdrawal'
        txid = self.safe_string(transaction, 'transaction_id')
        tag = None
        address = self.safe_string(transaction, 'address')
        if address is not None:
            addressParts = address.split('?dt=')
            numParts = len(addressParts)
            if numParts > 1:
                address = addressParts[0]
                tag = addressParts[1]
        addressFrom = None
        addressTo = address
        tagFrom = None
        tagTo = tag
        fee = None
        if feeCost is not None:
            fee = {'currency': feeCurrency, 'cost': feeCost, 'rate': None}
        return {'info': transaction, 'id': id, 'txid': txid, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'network': None, 'addressFrom': addressFrom, 'addressTo': addressTo, 'address': address, 'tagFrom': tagFrom, 'tagTo': tagTo, 'tag': tag, 'type': type, 'amount': amount, 'currency': code, 'status': status, 'updated': None, 'fee': fee}

    def parse_transaction_status(self, status):
        statuses = {'0': 'pending', '1': 'pending', '2': 'ok', '3': 'canceled', '4': 'failed'}
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        clientOrderId = self.safe_string(order, 'client_order_id')
        side = self.safe_string(order, 'type')
        if side is not None:
            side = 'sell' if side == '1' else 'buy'
        timestamp = self.parse8601(self.safe_string(order, 'datetime'))
        marketId = self.safe_string_lower(order, 'currency_pair')
        symbol = self.safe_symbol(marketId, market, '/')
        status = self.parse_order_status(self.safe_string(order, 'status'))
        amount = self.safe_string(order, 'amount')
        transactions = self.safe_value(order, 'transactions', [])
        price = self.safe_string(order, 'price')
        return self.safe_order({'id': id, 'clientOrderId': clientOrderId, 'datetime': self.iso8601(timestamp), 'timestamp': timestamp, 'lastTradeTimestamp': None, 'status': status, 'symbol': symbol, 'type': None, 'timeInForce': None, 'postOnly': None, 'side': side, 'price': price, 'stopPrice': None, 'cost': None, 'amount': amount, 'filled': None, 'remaining': None, 'trades': transactions, 'fee': None, 'info': order, 'average': None}, market)

    def parse_ledger_entry_type(self, type):
        types = {'0': 'transaction', '1': 'transaction', '2': 'trade', '14': 'transfer'}
        return self.safe_string(types, type, type)

    def parse_ledger_entry(self, item, currency=None):
        type = self.parse_ledger_entry_type(self.safe_string(item, 'type'))
        if type == 'trade':
            parsedTrade = self.parse_trade(item)
            market = None
            keys = list(item.keys())
            for i in range(0, len(keys)):
                if keys[i].find('_') >= 0:
                    marketId = keys[i].replace('_', '')
                    if marketId in self.markets_by_id:
                        market = self.markets_by_id[marketId]
            if market is None:
                market = self.get_market_from_trade(item)
            direction = 'in' if parsedTrade['side'] == 'buy' else 'out'
            return {'id': parsedTrade['id'], 'info': item, 'timestamp': parsedTrade['timestamp'], 'datetime': parsedTrade['datetime'], 'direction': direction, 'account': None, 'referenceId': parsedTrade['order'], 'referenceAccount': None, 'type': type, 'currency': market['base'], 'amount': parsedTrade['amount'], 'before': None, 'after': None, 'status': 'ok', 'fee': parsedTrade['fee']}
        else:
            parsedTransaction = self.parse_transaction(item, currency)
            direction = None
            if 'amount' in item:
                amount = self.safe_number(item, 'amount')
                direction = 'in' if amount > 0 else 'out'
            elif 'currency' in parsedTransaction and parsedTransaction['currency'] is not None:
                currencyCode = self.safe_string(parsedTransaction, 'currency')
                currency = self.currency(currencyCode)
                amount = self.safe_number(item, currency['id'])
                direction = 'in' if amount > 0 else 'out'
            return {'id': parsedTransaction['id'], 'info': item, 'timestamp': parsedTransaction['timestamp'], 'datetime': parsedTransaction['datetime'], 'direction': direction, 'account': None, 'referenceId': parsedTransaction['txid'], 'referenceAccount': None, 'type': type, 'currency': parsedTransaction['currency'], 'amount': parsedTransaction['amount'], 'before': None, 'after': None, 'status': parsedTransaction['status'], 'fee': parsedTransaction['fee']}

    def fetch_ledger(self, code=None, since=None, limit=None, params={}):
        """
        fetch the history of changes, actions done by the user or operations that altered balance of the user
        :param str|None code: unified currency code, default is None
        :param int|None since: timestamp in ms of the earliest ledger entry, default is None
        :param int|None limit: max number of ledger entrys to return, default is None
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a `ledger structure <https://docs.ccxt.com/en/latest/manual.html#ledger-structure>`
        """
        self.load_markets()
        request = {}
        if limit is not None:
            request['limit'] = limit
        response = self.privatePostUserTransactions(self.extend(request, params))
        currency = None
        if code is not None:
            currency = self.currency(code)
        return self.parse_ledger(response, currency, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        market = None
        self.load_markets()
        if symbol is not None:
            market = self.market(symbol)
        response = self.privatePostOpenOrdersAll(params)
        return self.parse_orders(response, market, since, limit, {'status': 'open', 'type': 'limit'})

    def get_currency_name(self, code):
        return code.lower()

    def is_fiat(self, code):
        return code == 'USD' or code == 'EUR' or code == 'GBP'

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        if self.is_fiat(code):
            raise NotSupported(self.id + ' fiat fetchDepositAddress() for ' + code + ' is not supported!')
        name = self.get_currency_name(code)
        method = 'privatePost' + self.capitalize(name) + 'Address'
        response = getattr(self, method)(params)
        address = self.safe_string(response, 'address')
        tag = self.safe_string_2(response, 'memo_id', 'destination_tag')
        self.check_address(address)
        return {'currency': code, 'address': address, 'tag': tag, 'network': None, 'info': response}

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the bitstamp api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        self.load_markets()
        self.check_address(address)
        request = {'amount': amount}
        currency = None
        method = None
        if not self.is_fiat(code):
            name = self.get_currency_name(code)
            method = 'privatePost' + self.capitalize(name) + 'Withdrawal'
            if code == 'XRP':
                if tag is not None:
                    request['destination_tag'] = tag
            elif code == 'XLM' or code == 'HBAR':
                if tag is not None:
                    request['memo_id'] = tag
            request['address'] = address
        else:
            method = 'privatePostWithdrawalOpen'
            currency = self.currency(code)
            request['iban'] = address
            request['account_currency'] = currency['id']
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_transaction(response, currency)

    def nonce(self):
        return self.milliseconds()

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        url += self.version + '/'
        url += self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            xAuth = 'BITSTAMP ' + self.apiKey
            xAuthNonce = self.uuid()
            xAuthTimestamp = str(self.milliseconds())
            xAuthVersion = 'v2'
            contentType = ''
            headers = {'X-Auth': xAuth, 'X-Auth-Nonce': xAuthNonce, 'X-Auth-Timestamp': xAuthTimestamp, 'X-Auth-Version': xAuthVersion}
            if method == 'POST':
                if query:
                    body = self.urlencode(query)
                    contentType = 'application/x-www-form-urlencoded'
                    headers['Content-Type'] = contentType
                else:
                    body = self.urlencode({'foo': 'bar'})
                    contentType = 'application/x-www-form-urlencoded'
                    headers['Content-Type'] = contentType
            authBody = body if body else ''
            auth = xAuth + method + url.replace('https://', '') + contentType + xAuthNonce + xAuthTimestamp + xAuthVersion + authBody
            signature = self.hmac(self.encode(auth), self.encode(self.secret))
            headers['X-Auth-Signature'] = signature
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        status = self.safe_string(response, 'status')
        error = self.safe_value(response, 'error')
        if status == 'error' or error is not None:
            errors = []
            if isinstance(error, str):
                errors.append(error)
            elif error is not None:
                keys = list(error.keys())
                for i in range(0, len(keys)):
                    key = keys[i]
                    value = self.safe_value(error, key)
                    if isinstance(value, list):
                        errors = self.array_concat(errors, value)
                    else:
                        errors.append(value)
            reason = self.safe_value(response, 'reason', {})
            if isinstance(reason, str):
                errors.append(reason)
            else:
                all = self.safe_value(reason, '__all__', [])
                for i in range(0, len(all)):
                    errors.append(all[i])
            code = self.safe_string(response, 'code')
            if code == 'API0005':
                raise AuthenticationError(self.id + ' invalid signature, use the uid for the main account if you have subaccounts')
            feedback = self.id + ' ' + body
            for i in range(0, len(errors)):
                value = errors[i]
                self.throw_exactly_matched_exception(self.exceptions['exact'], value, feedback)
                self.throw_broadly_matched_exception(self.exceptions['broad'], value, feedback)
            raise ExchangeError(feedback)