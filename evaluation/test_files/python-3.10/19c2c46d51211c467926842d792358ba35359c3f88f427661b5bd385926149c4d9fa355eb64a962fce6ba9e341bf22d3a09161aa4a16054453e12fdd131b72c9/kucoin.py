from ccxt.base.exchange import Exchange
import hashlib
import math
import json
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import AccountSuspended
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import InvalidNonce
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise

class kucoin(Exchange):

    def describe(self):
        return self.deep_extend(super(kucoin, self).describe(), {'id': 'kucoin', 'name': 'KuCoin', 'countries': ['SC'], 'rateLimit': 50, 'version': 'v2', 'certified': True, 'pro': True, 'comment': 'Platform 2.0', 'quoteJsonNumbers': False, 'has': {'CORS': None, 'spot': True, 'margin': True, 'swap': False, 'future': False, 'option': None, 'borrowMargin': True, 'cancelAllOrders': True, 'cancelOrder': True, 'createDepositAddress': True, 'createOrder': True, 'createStopLimitOrder': True, 'createStopMarketOrder': True, 'createStopOrder': True, 'fetchAccounts': True, 'fetchBalance': True, 'fetchBorrowInterest': True, 'fetchBorrowRate': False, 'fetchBorrowRateHistories': False, 'fetchBorrowRateHistory': True, 'fetchBorrowRates': False, 'fetchClosedOrders': True, 'fetchCurrencies': True, 'fetchDepositAddress': True, 'fetchDepositAddressesByNetwork': True, 'fetchDeposits': True, 'fetchDepositWithdrawFee': True, 'fetchDepositWithdrawFees': False, 'fetchFundingHistory': False, 'fetchFundingRate': False, 'fetchFundingRateHistory': False, 'fetchFundingRates': False, 'fetchIndexOHLCV': False, 'fetchL3OrderBook': True, 'fetchLedger': True, 'fetchMarginMode': False, 'fetchMarkets': True, 'fetchMarkOHLCV': False, 'fetchMyTrades': True, 'fetchOHLCV': True, 'fetchOpenInterestHistory': False, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchOrdersByStatus': True, 'fetchOrderTrades': True, 'fetchPositionMode': False, 'fetchPremiumIndexOHLCV': False, 'fetchStatus': True, 'fetchTicker': True, 'fetchTickers': True, 'fetchTime': True, 'fetchTrades': True, 'fetchTradingFee': True, 'fetchTradingFees': False, 'fetchTransactionFee': True, 'fetchWithdrawals': True, 'repayMargin': True, 'setMarginMode': False, 'transfer': True, 'withdraw': True}, 'urls': {'logo': 'https://user-images.githubusercontent.com/51840849/87295558-132aaf80-c50e-11ea-9801-a2fb0c57c799.jpg', 'referral': 'https://www.kucoin.com/ucenter/signup?rcode=E5wkqe', 'api': {'public': 'https://api.kucoin.com', 'private': 'https://api.kucoin.com', 'futuresPrivate': 'https://api-futures.kucoin.com', 'futuresPublic': 'https://api-futures.kucoin.com'}, 'test': {'public': 'https://openapi-sandbox.kucoin.com', 'private': 'https://openapi-sandbox.kucoin.com', 'futuresPrivate': 'https://api-sandbox-futures.kucoin.com', 'futuresPublic': 'https://api-sandbox-futures.kucoin.com'}, 'www': 'https://www.kucoin.com', 'doc': ['https://docs.kucoin.com']}, 'requiredCredentials': {'apiKey': True, 'secret': True, 'password': True}, 'api': {'public': {'get': {'timestamp': 1, 'status': 1, 'symbols': 1, 'markets': 1, 'market/allTickers': 1, 'market/orderbook/level{level}_{limit}': 1, 'market/orderbook/level2_20': 1, 'market/orderbook/level2_100': 1, 'market/histories': 1, 'market/candles': 1, 'market/stats': 1, 'currencies': 1, 'currencies/{currency}': 1, 'prices': 1, 'mark-price/{symbol}/current': 1, 'margin/config': 1, 'margin/trade/last': 1}, 'post': {'bullet-public': 1}}, 'private': {'get': {'market/orderbook/level{level}': 1, 'market/orderbook/level2': {'v3': 2}, 'market/orderbook/level3': 1, 'accounts': 1, 'accounts/{accountId}': 1, 'accounts/ledgers': 3.333, 'accounts/{accountId}/holds': 1, 'accounts/transferable': 1, 'base-fee': 1, 'sub/user': 1, 'user-info': 1, 'sub/api-key': 1, 'sub-accounts': 1, 'sub-accounts/{subUserId}': 1, 'deposit-addresses': 1, 'deposits': 10, 'hist-deposits': 10, 'hist-withdrawals': 10, 'withdrawals': 10, 'withdrawals/quotas': 1, 'orders': 2, 'order/client-order/{clientOid}': 1, 'orders/{orderId}': 1, 'limit/orders': 1, 'fills': 6.66667, 'limit/fills': 1, 'isolated/accounts': 2, 'isolated/account/{symbol}': 2, 'isolated/borrow/outstanding': 2, 'isolated/borrow/repaid': 2, 'isolated/symbols': 2, 'margin/account': 1, 'margin/borrow': 1, 'margin/borrow/outstanding': 1, 'margin/borrow/repaid': 1, 'margin/lend/active': 1, 'margin/lend/done': 1, 'margin/lend/trade/unsettled': 1, 'margin/lend/trade/settled': 1, 'margin/lend/assets': 1, 'margin/market': 1, 'stop-order/{orderId}': 1, 'stop-order': 1, 'stop-order/queryOrderByClientOid': 1, 'trade-fees': 1.3333}, 'post': {'accounts': 1, 'accounts/inner-transfer': {'v2': 1}, 'accounts/sub-transfer': {'v2': 25}, 'deposit-addresses': 1, 'withdrawals': 1, 'orders': 4, 'orders/multi': 20, 'isolated/borrow': 2, 'isolated/repay/all': 2, 'isolated/repay/single': 2, 'margin/borrow': 1, 'margin/order': 1, 'margin/repay/all': 1, 'margin/repay/single': 1, 'margin/lend': 1, 'margin/toggle-auto-lend': 1, 'bullet-private': 1, 'stop-order': 1, 'sub/user': 1, 'sub/api-key': 1, 'sub/api-key/update': 1}, 'delete': {'withdrawals/{withdrawalId}': 1, 'orders': 20, 'order/client-order/{clientOid}': 1, 'orders/{orderId}': 1, 'margin/lend/{orderId}': 1, 'stop-order/cancelOrderByClientOid': 1, 'stop-order/{orderId}': 1, 'stop-order/cancel': 1, 'sub/api-key': 1}}, 'futuresPublic': {'get': {'contracts/active': 1.3953, 'contracts/{symbol}': 1.3953, 'ticker': 1.3953, 'level2/snapshot': 2, 'level2/depth20': 1.3953, 'level2/depth100': 1.3953, 'level2/message/query': 1.3953, 'level3/message/query': 1.3953, 'level3/snapshot': 1.3953, 'trade/history': 1.3953, 'interest/query': 1.3953, 'index/query': 1.3953, 'mark-price/{symbol}/current': 1.3953, 'premium/query': 1.3953, 'funding-rate/{symbol}/current': 1.3953, 'timestamp': 1.3953, 'status': 1.3953, 'kline/query': 1.3953}, 'post': {'bullet-public': 1.3953}}, 'futuresPrivate': {'get': {'account-overview': 2, 'transaction-history': 6.666, 'deposit-address': 1.3953, 'deposit-list': 1.3953, 'withdrawals/quotas': 1.3953, 'withdrawal-list': 1.3953, 'transfer-list': 1.3953, 'orders': 1.3953, 'stopOrders': 1.3953, 'recentDoneOrders': 1.3953, 'orders/{orderId}': 1.3953, 'orders/byClientOid': 1.3953, 'fills': 6.666, 'recentFills': 6.666, 'openOrderStatistics': 1.3953, 'position': 1.3953, 'positions': 6.666, 'funding-history': 6.666}, 'post': {'withdrawals': 1.3953, 'transfer-out': 1.3953, 'orders': 1.3953, 'position/margin/auto-deposit-status': 1.3953, 'position/margin/deposit-margin': 1.3953, 'bullet-private': 1.3953}, 'delete': {'withdrawals/{withdrawalId}': 1.3953, 'cancel/transfer-out': 1.3953, 'orders/{orderId}': 1.3953, 'orders': 6.666, 'stopOrders': 1.3953}}}, 'timeframes': {'1m': '1min', '3m': '3min', '5m': '5min', '15m': '15min', '30m': '30min', '1h': '1hour', '2h': '2hour', '4h': '4hour', '6h': '6hour', '8h': '8hour', '12h': '12hour', '1d': '1day', '1w': '1week'}, 'precisionMode': TICK_SIZE, 'exceptions': {'exact': {'order not exist': OrderNotFound, 'order not exist.': OrderNotFound, 'order_not_exist': OrderNotFound, 'order_not_exist_or_not_allow_to_cancel': InvalidOrder, 'Order size below the minimum requirement.': InvalidOrder, 'The withdrawal amount is below the minimum requirement.': ExchangeError, 'Unsuccessful! Exceeded the max. funds out-transfer limit': InsufficientFunds, '400': BadRequest, '401': AuthenticationError, '403': NotSupported, '404': NotSupported, '405': NotSupported, '429': RateLimitExceeded, '500': ExchangeNotAvailable, '503': ExchangeNotAvailable, '101030': PermissionDenied, '103000': InvalidOrder, '200004': InsufficientFunds, '210014': InvalidOrder, '210021': InsufficientFunds, '230003': InsufficientFunds, '260000': InvalidAddress, '260100': InsufficientFunds, '300000': InvalidOrder, '400000': BadSymbol, '400001': AuthenticationError, '400002': InvalidNonce, '400003': AuthenticationError, '400004': AuthenticationError, '400005': AuthenticationError, '400006': AuthenticationError, '400007': AuthenticationError, '400008': NotSupported, '400100': BadRequest, '400200': InvalidOrder, '400350': InvalidOrder, '400370': InvalidOrder, '400500': InvalidOrder, '400600': BadSymbol, '400760': InvalidOrder, '401000': BadRequest, '411100': AccountSuspended, '415000': BadRequest, '500000': ExchangeNotAvailable, '260220': InvalidAddress, '900014': BadRequest}, 'broad': {'Exceeded the access frequency': RateLimitExceeded, 'require more permission': PermissionDenied}}, 'fees': {'trading': {'tierBased': True, 'percentage': True, 'taker': self.parse_number('0.001'), 'maker': self.parse_number('0.001'), 'tiers': {'taker': [[self.parse_number('0'), self.parse_number('0.001')], [self.parse_number('50'), self.parse_number('0.001')], [self.parse_number('200'), self.parse_number('0.0009')], [self.parse_number('500'), self.parse_number('0.0008')], [self.parse_number('1000'), self.parse_number('0.0007')], [self.parse_number('2000'), self.parse_number('0.0007')], [self.parse_number('4000'), self.parse_number('0.0006')], [self.parse_number('8000'), self.parse_number('0.0005')], [self.parse_number('15000'), self.parse_number('0.00045')], [self.parse_number('25000'), self.parse_number('0.0004')], [self.parse_number('40000'), self.parse_number('0.00035')], [self.parse_number('60000'), self.parse_number('0.0003')], [self.parse_number('80000'), self.parse_number('0.00025')]], 'maker': [[self.parse_number('0'), self.parse_number('0.001')], [self.parse_number('50'), self.parse_number('0.0009')], [self.parse_number('200'), self.parse_number('0.0007')], [self.parse_number('500'), self.parse_number('0.0005')], [self.parse_number('1000'), self.parse_number('0.0003')], [self.parse_number('2000'), self.parse_number('0')], [self.parse_number('4000'), self.parse_number('0')], [self.parse_number('8000'), self.parse_number('0')], [self.parse_number('15000'), self.parse_number('-0.00005')], [self.parse_number('25000'), self.parse_number('-0.00005')], [self.parse_number('40000'), self.parse_number('-0.00005')], [self.parse_number('60000'), self.parse_number('-0.00005')], [self.parse_number('80000'), self.parse_number('-0.00005')]]}}, 'funding': {'tierBased': False, 'percentage': False, 'withdraw': {}, 'deposit': {}}}, 'commonCurrencies': {'BIFI': 'BIFIF', 'EDGE': 'DADI', 'HOT': 'HOTNOW', 'TRY': 'Trias', 'VAI': 'VAIOT', 'WAX': 'WAXP'}, 'options': {'version': 'v1', 'symbolSeparator': '-', 'fetchMyTradesMethod': 'private_get_fills', 'fetchMarkets': {'fetchTickersFees': True}, 'versions': {'public': {'GET': {'currencies/{currency}': 'v2', 'status': 'v1', 'market/orderbook/level2_20': 'v1', 'market/orderbook/level2_100': 'v1', 'market/orderbook/level{level}_{limit}': 'v1'}}, 'private': {'GET': {'market/orderbook/level2': 'v3', 'market/orderbook/level3': 'v3', 'market/orderbook/level{level}': 'v3', 'deposit-addresses': 'v1'}, 'POST': {'accounts/inner-transfer': 'v2', 'accounts/sub-transfer': 'v2', 'accounts': 'v2'}}, 'futuresPrivate': {'GET': {'account-overview': 'v1', 'positions': 'v1'}, 'POST': {'transfer-out': 'v2'}}, 'futuresPublic': {'GET': {'level3/snapshot': 'v2'}}}, 'partner': {'spot': {'id': 'ccxt', 'key': '9e58cc35-5b5e-4133-92ec-166e3f077cb8'}, 'future': {'id': 'ccxtfutures', 'key': '1b327198-f30c-4f14-a0ac-918871282f15'}}, 'accountsByType': {'spot': 'trade', 'margin': 'margin', 'cross': 'margin', 'isolated': 'isolated', 'main': 'main', 'funding': 'main', 'future': 'contract', 'swap': 'contract', 'mining': 'pool'}, 'networks': {'Native': 'bech32', 'BTC-Segwit': 'btc', 'ERC20': 'eth', 'BEP20': 'bsc', 'TRC20': 'trx', 'TERRA': 'luna', 'BNB': 'bsc', 'HRC20': 'heco', 'HT': 'heco'}, 'networksById': {'BEP20': 'BSC'}}})

    def nonce(self):
        return self.milliseconds()

    def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        response = self.publicGetTimestamp(params)
        return self.safe_integer(response, 'data')

    def fetch_status(self, params={}):
        """
        the latest known information on the availability of the exchange API
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `status structure <https://docs.ccxt.com/en/latest/manual.html#exchange-status-structure>`
        """
        response = self.publicGetStatus(params)
        data = self.safe_value(response, 'data', {})
        status = self.safe_string(data, 'status')
        return {'status': 'ok' if status == 'open' else 'maintenance', 'updated': None, 'eta': None, 'url': None, 'info': response}

    def fetch_markets(self, params={}):
        """
        retrieves data on all markets for kucoin
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        response = self.publicGetSymbols(params)
        data = self.safe_value(response, 'data')
        options = self.safe_value(self.options, 'fetchMarkets', {})
        fetchTickersFees = self.safe_value(options, 'fetchTickersFees', True)
        tickersResponse = {}
        if fetchTickersFees:
            tickersResponse = self.publicGetMarketAllTickers(params)
        tickersData = self.safe_value(tickersResponse, 'data', {})
        tickers = self.safe_value(tickersData, 'ticker', [])
        tickersByMarketId = self.index_by(tickers, 'symbol')
        result = []
        for i in range(0, len(data)):
            market = data[i]
            id = self.safe_string(market, 'symbol')
            (baseId, quoteId) = id.split('-')
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            ticker = self.safe_value(tickersByMarketId, id, {})
            makerFeeRate = self.safe_string(ticker, 'makerFeeRate')
            takerFeeRate = self.safe_string(ticker, 'takerFeeRate')
            makerCoefficient = self.safe_string(ticker, 'makerCoefficient')
            takerCoefficient = self.safe_string(ticker, 'takerCoefficient')
            result.append({'id': id, 'symbol': base + '/' + quote, 'base': base, 'quote': quote, 'settle': None, 'baseId': baseId, 'quoteId': quoteId, 'settleId': None, 'type': 'spot', 'spot': True, 'margin': self.safe_value(market, 'isMarginEnabled'), 'swap': False, 'future': False, 'option': False, 'active': self.safe_value(market, 'enableTrading'), 'contract': False, 'linear': None, 'inverse': None, 'taker': self.parse_number(Precise.string_mul(takerFeeRate, takerCoefficient)), 'maker': self.parse_number(Precise.string_mul(makerFeeRate, makerCoefficient)), 'contractSize': None, 'expiry': None, 'expiryDatetime': None, 'strike': None, 'optionType': None, 'precision': {'amount': self.safe_number(market, 'baseIncrement'), 'price': self.safe_number(market, 'priceIncrement')}, 'limits': {'leverage': {'min': None, 'max': None}, 'amount': {'min': self.safe_number(market, 'baseMinSize'), 'max': self.safe_number(market, 'baseMaxSize')}, 'price': {'min': None, 'max': None}, 'cost': {'min': self.safe_number(market, 'quoteMinSize'), 'max': self.safe_number(market, 'quoteMaxSize')}}, 'info': market})
        return result

    def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = self.publicGetCurrencies(params)
        data = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(data)):
            entry = data[i]
            id = self.safe_string(entry, 'currency')
            name = self.safe_string(entry, 'fullName')
            code = self.safe_currency_code(id)
            isWithdrawEnabled = self.safe_value(entry, 'isWithdrawEnabled', False)
            isDepositEnabled = self.safe_value(entry, 'isDepositEnabled', False)
            fee = self.safe_number(entry, 'withdrawalMinFee')
            active = isWithdrawEnabled and isDepositEnabled
            result[code] = {'id': id, 'name': name, 'code': code, 'precision': self.parse_number(self.parse_precision(self.safe_string(entry, 'precision'))), 'info': entry, 'active': active, 'deposit': isDepositEnabled, 'withdraw': isWithdrawEnabled, 'fee': fee, 'limits': self.limits}
        return result

    def fetch_accounts(self, params={}):
        """
        fetch all the accounts associated with a profile
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a dictionary of `account structures <https://docs.ccxt.com/en/latest/manual.html#account-structure>` indexed by the account type
        """
        response = self.privateGetAccounts(params)
        data = self.safe_value(response, 'data', [])
        result = []
        for i in range(0, len(data)):
            account = data[i]
            accountId = self.safe_string(account, 'id')
            currencyId = self.safe_string(account, 'currency')
            code = self.safe_currency_code(currencyId)
            type = self.safe_string(account, 'type')
            result.append({'id': accountId, 'type': type, 'currency': code, 'info': account})
        return result

    def fetch_transaction_fee(self, code, params={}):
        """
        *DEPRECATED* please use fetchDepositWithdrawFee instead
        see https://docs.kucoin.com/#get-withdrawal-quotas
        :param str code: unified currency code
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper_2(params, 'network', 'chain')
        network = self.safe_string_lower(networks, network, network)
        if network is not None:
            network = network.lower()
            request['chain'] = network.lower()
            params = self.omit(params, ['network', 'chain'])
        response = self.privateGetWithdrawalsQuotas(self.extend(request, params))
        data = response['data']
        withdrawFees = {}
        withdrawFees[code] = self.safe_number(data, 'withdrawMinFee')
        return {'info': response, 'withdraw': withdrawFees, 'deposit': {}}

    def fetch_deposit_withdraw_fee(self, code, params={}):
        """
        fetch the fee for deposits and withdrawals
        see https://docs.kucoin.com/#get-withdrawal-quotas
        :param str code: unified currency code
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param str|None params['network']: The chain of currency. This only apply for multi-chain currency, and there is no need for single chain currency; you can query the chain through the response of the GET /api/v2/currencies/{currency} interface
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        networkCode = self.safe_string_upper(params, 'network')
        network = self.network_code_to_id(networkCode, code)
        if network is not None:
            request['chain'] = network
            params = self.omit(params, ['network'])
        response = self.privateGetWithdrawalsQuotas(self.extend(request, params))
        data = self.safe_value(response, 'data')
        return self.parse_deposit_withdraw_fee(data, currency)

    def parse_deposit_withdraw_fee(self, fee, currency=None):
        result = self.deposit_withdraw_fee(fee)
        isWithdrawEnabled = self.safe_value(fee, 'isWithdrawEnabled')
        if isWithdrawEnabled:
            networkId = self.safe_string(fee, 'chain')
            networkCode = self.network_id_to_code(networkId, self.safe_string(currency, 'code'))
            result['networks'][networkCode] = {'withdraw': {'fee': self.safe_number(fee, 'withdrawMinFee'), 'percentage': None}, 'deposit': {'fee': None, 'percentage': None}}
        return self.assign_default_deposit_withdraw_fees(result)

    def is_futures_method(self, methodName, params):
        defaultType = self.safe_string_2(self.options, methodName, 'defaultType', 'trade')
        requestedType = self.safe_string(params, 'type', defaultType)
        accountsByType = self.safe_value(self.options, 'accountsByType')
        type = self.safe_string(accountsByType, requestedType)
        if type is None:
            keys = list(accountsByType.keys())
            raise ExchangeError(self.id + ' isFuturesMethod() type must be one of ' + ', '.join(keys))
        params = self.omit(params, 'type')
        return type == 'contract' or type == 'future' or type == 'futures'

    def parse_ticker(self, ticker, market=None):
        percentage = self.safe_string(ticker, 'changeRate')
        if percentage is not None:
            percentage = Precise.string_mul(percentage, '100')
        last = self.safe_string_2(ticker, 'last', 'lastTradedPrice')
        last = self.safe_string(ticker, 'price', last)
        marketId = self.safe_string(ticker, 'symbol')
        market = self.safe_market(marketId, market, '-')
        symbol = market['symbol']
        baseVolume = self.safe_string(ticker, 'vol')
        quoteVolume = self.safe_string(ticker, 'volValue')
        timestamp = self.safe_integer_2(ticker, 'time', 'datetime')
        return self.safe_ticker({'symbol': symbol, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'high': self.safe_string(ticker, 'high'), 'low': self.safe_string(ticker, 'low'), 'bid': self.safe_string_2(ticker, 'buy', 'bestBid'), 'bidVolume': self.safe_string(ticker, 'bestBidSize'), 'ask': self.safe_string_2(ticker, 'sell', 'bestAsk'), 'askVolume': self.safe_string(ticker, 'bestAskSize'), 'vwap': None, 'open': self.safe_string(ticker, 'open'), 'close': last, 'last': last, 'previousClose': None, 'change': self.safe_string(ticker, 'changePrice'), 'percentage': percentage, 'average': self.safe_string(ticker, 'averagePrice'), 'baseVolume': baseVolume, 'quoteVolume': quoteVolume, 'info': ticker}, market)

    def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        symbols = self.market_symbols(symbols)
        response = self.publicGetMarketAllTickers(params)
        data = self.safe_value(response, 'data', {})
        tickers = self.safe_value(data, 'ticker', [])
        time = self.safe_integer(data, 'time')
        result = {}
        for i in range(0, len(tickers)):
            tickers[i]['time'] = time
            ticker = self.parse_ticker(tickers[i])
            symbol = self.safe_string(ticker, 'symbol')
            if symbol is not None:
                result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        response = self.publicGetMarketStats(self.extend(request, params))
        return self.parse_ticker(response['data'], market)

    def parse_ohlcv(self, ohlcv, market=None):
        return [self.safe_timestamp(ohlcv, 0), self.safe_number(ohlcv, 1), self.safe_number(ohlcv, 3), self.safe_number(ohlcv, 4), self.safe_number(ohlcv, 2), self.safe_number(ohlcv, 5)]

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        self.load_markets()
        market = self.market(symbol)
        marketId = market['id']
        request = {'symbol': marketId, 'type': self.timeframes[timeframe]}
        duration = self.parse_timeframe(timeframe) * 1000
        endAt = self.milliseconds()
        if since is not None:
            request['startAt'] = int(int(math.floor(since / 1000)))
            if limit is None:
                limit = self.safe_integer(self.options, 'fetchOHLCVLimit', 1500)
            endAt = self.sum(since, limit * duration)
        elif limit is not None:
            since = endAt - limit * duration
            request['startAt'] = int(int(math.floor(since / 1000)))
        request['endAt'] = int(int(math.floor(endAt / 1000)))
        response = self.publicGetMarketCandles(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def create_deposit_address(self, code, params={}):
        """
        see https://docs.kucoin.com/#create-deposit-address
        create a currency deposit address
        :param str code: unified currency code of the currency for the deposit address
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param str|None params['network']: the blockchain network name
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper_2(params, 'chain', 'network')
        network = self.safe_string_lower(networks, network, network)
        if network is not None:
            network = network.lower()
            request['chain'] = network
            params = self.omit(params, ['chain', 'network'])
        response = self.privatePostDepositAddresses(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        address = self.safe_string(data, 'address')
        if address is not None:
            address = address.replace('bitcoincash:', '')
        tag = self.safe_string(data, 'memo')
        if code != 'NIM':
            self.check_address(address)
        return {'info': response, 'currency': code, 'network': self.safe_string(data, 'chain'), 'address': address, 'tag': tag}

    def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param str|None params['network']: the blockchain network name
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper_2(params, 'chain', 'network')
        network = self.safe_string_lower(networks, network, network)
        if network is not None:
            network = network.lower()
            request['chain'] = network
            params = self.omit(params, ['chain', 'network'])
        version = self.options['versions']['private']['GET']['deposit-addresses']
        self.options['versions']['private']['GET']['deposit-addresses'] = 'v1'
        response = self.privateGetDepositAddresses(self.extend(request, params))
        self.options['versions']['private']['GET']['deposit-addresses'] = version
        data = self.safe_value(response, 'data', {})
        return self.parse_deposit_address(data, currency)

    def parse_deposit_address(self, depositAddress, currency=None):
        address = self.safe_string(depositAddress, 'address')
        code = currency['id']
        if code != 'NIM':
            self.check_address(address)
        return {'info': depositAddress, 'currency': code, 'address': address, 'tag': self.safe_string(depositAddress, 'memo'), 'network': self.safe_string(depositAddress, 'chain')}

    def fetch_deposit_addresses_by_network(self, code, params={}):
        """
        see https://docs.kucoin.com/#get-deposit-addresses-v2
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: an array of `address structures <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        version = self.options['versions']['private']['GET']['deposit-addresses']
        self.options['versions']['private']['GET']['deposit-addresses'] = 'v2'
        response = self.privateGetDepositAddresses(self.extend(request, params))
        self.options['versions']['private']['GET']['deposit-addresses'] = version
        data = self.safe_value(response, 'data', [])
        return self.parse_deposit_addresses_by_network(data, currency)

    def parse_deposit_addresses_by_network(self, depositAddresses, currency=None):
        result = []
        for i in range(0, len(depositAddresses)):
            entry = depositAddresses[i]
            result.append({'info': entry, 'currency': self.safe_currency_code(currency['id'], currency), 'network': self.safe_string(entry, 'chain'), 'address': self.safe_string(entry, 'address'), 'tag': self.safe_string(entry, 'memo')})
        return result

    def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        market = self.market(symbol)
        level = self.safe_integer(params, 'level', 2)
        request = {'symbol': market['id']}
        method = 'publicGetMarketOrderbookLevelLevelLimit'
        isAuthenticated = self.check_required_credentials(False)
        response = None
        if not isAuthenticated or limit is not None:
            if level == 2:
                request['level'] = level
                if limit is not None:
                    if limit == 20 or limit == 100:
                        request['limit'] = limit
                    else:
                        raise ExchangeError(self.id + ' fetchOrderBook() limit argument must be 20 or 100')
                request['limit'] = limit if limit else 100
        else:
            method = 'privateGetMarketOrderbookLevel2'
        response = getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(data, 'time')
        orderbook = self.parse_order_book(data, market['symbol'], timestamp, 'bids', 'asks', level - 2, level - 1)
        orderbook['nonce'] = self.safe_integer(data, 'sequence')
        return orderbook

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        Create an order on the exchange
        :param str symbol: Unified CCXT market symbol
        :param str type: 'limit' or 'market'
        :param str side: 'buy' or 'sell'
        :param float amount: the amount of currency to trade
        :param float price: *ignored in "market" orders* the price at which the order is to be fullfilled at in units of the quote currency
        :param dict params:  Extra parameters specific to the exchange API endpoint
        :param str params['clientOid']: client order id, defaults to uuid if not passed
        :param str params['remark']: remark for the order, length cannot exceed 100 utf8 characters
        :param str params['tradeType']: 'TRADE',  # TRADE, MARGIN_TRADE  # not used with margin orders
         * limit orders ---------------------------------------------------
        :param str params['timeInForce']: GTC, GTT, IOC, or FOK, default is GTC, limit orders only
        :param float params['cancelAfter']: long,  # cancel after n seconds, requires timeInForce to be GTT
        :param str params['postOnly']: Post only flag, invalid when timeInForce is IOC or FOK
        :param bool params['hidden']: False,  # Order will not be displayed in the order book
        :param bool params['iceberg']: False,  # Only a portion of the order is displayed in the order book
        :param str params['visibleSize']: self.amount_to_precision(symbol, visibleSize),  # The maximum visible size of an iceberg order
         * market orders --------------------------------------------------
        :param str params['funds']:  # Amount of quote currency to use
         * stop orders ----------------------------------------------------
        :param str params['stop']:  Either loss or entry, the default is loss. Requires stopPrice to be defined
        :param float params['stopPrice']: The price at which a trigger order is triggered at
         * margin orders --------------------------------------------------
        :param float params['leverage']: Leverage size of the order
        :param str params['stp']: '',  # self trade prevention, CN, CO, CB or DC
        :param str params['marginMode']: 'cross',  # cross(cross mode) and isolated(isolated mode), set to cross by default, the isolated mode will be released soon, stay tuned
        :param bool params['autoBorrow']: False,  # The system will first borrow you funds at the optimal interest rate and then place an order for you
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        marketId = self.market_id(symbol)
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId', self.uuid())
        params = self.omit(params, ['clientOid', 'clientOrderId'])
        request = {'clientOid': clientOrderId, 'side': side, 'symbol': marketId, 'type': type}
        quoteAmount = self.safe_number_2(params, 'cost', 'funds')
        amountString = None
        costString = None
        marginMode = None
        (marginMode, params) = self.handle_margin_mode_and_params('createOrder', params)
        if type == 'market':
            if quoteAmount is not None:
                params = self.omit(params, ['cost', 'funds'])
                costString = self.amount_to_precision(symbol, quoteAmount)
                request['funds'] = costString
            else:
                amountString = self.amount_to_precision(symbol, amount)
                request['size'] = self.amount_to_precision(symbol, amount)
        else:
            amountString = self.amount_to_precision(symbol, amount)
            request['size'] = amountString
            request['price'] = self.price_to_precision(symbol, price)
        stopLossPrice = self.safe_value(params, 'stopLossPrice')
        takeProfitPrice = self.safe_value_2(params, 'takeProfitPrice', 'stopPrice')
        isStopLoss = stopLossPrice is not None
        isTakeProfit = takeProfitPrice is not None
        if isStopLoss and isTakeProfit:
            raise ExchangeError(self.id + ' createOrder() stopLossPrice and takeProfitPrice cannot both be defined')
        params = self.omit(params, ['stopLossPrice', 'takeProfitPrice', 'stopPrice'])
        tradeType = self.safe_string(params, 'tradeType')
        method = 'privatePostOrders'
        if isStopLoss or isTakeProfit:
            request['stop'] = 'entry' if isStopLoss else 'loss'
            triggerPrice = stopLossPrice if isStopLoss else takeProfitPrice
            request['stopPrice'] = self.price_to_precision(symbol, triggerPrice)
            method = 'privatePostStopOrder'
        elif tradeType == 'MARGIN_TRADE' or marginMode is not None:
            method = 'privatePostMarginOrder'
            if marginMode == 'isolated':
                request['marginModel'] = 'isolated'
        response = getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        timestamp = self.milliseconds()
        id = self.safe_string(data, 'orderId')
        order = {'id': id, 'clientOrderId': clientOrderId, 'info': data, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'lastTradeTimestamp': None, 'symbol': symbol, 'type': type, 'side': side, 'price': price, 'amount': self.parse_number(amountString), 'cost': self.parse_number(costString), 'average': None, 'filled': None, 'remaining': None, 'status': None, 'fee': None, 'trades': None}
        return order

    def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param bool params['stop']: True if cancelling a stop order
        :returns: Response from the exchange
        """
        self.load_markets()
        request = {}
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
        stop = self.safe_value(params, 'stop')
        method = 'privateDeleteOrdersOrderId'
        if clientOrderId is not None:
            request['clientOid'] = clientOrderId
            if stop:
                method = 'privateDeleteStopOrderCancelOrderByClientOid'
            else:
                method = 'privateDeleteOrderClientOrderClientOid'
        else:
            if stop:
                method = 'privateDeleteStopOrderOrderId'
            request['orderId'] = id
        params = self.omit(params, ['clientOid', 'clientOrderId', 'stop'])
        return getattr(self, method)(self.extend(request, params))

    def cancel_all_orders(self, symbol=None, params={}):
        """
        cancel all open orders
        :param str|None symbol: unified market symbol, only orders in the market of self symbol are cancelled when symbol is not None
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param bool params['stop']: True if cancelling all stop orders
        :param str params['tradeType']: The type of trading, "TRADE" for Spot Trading, "MARGIN_TRADE" for Margin Trading
        :param str params['orderIds']: *stop orders only* Comma seperated order IDs
        :returns: Response from the exchange
        """
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        method = 'privateDeleteOrders'
        stop = self.safe_value(params, 'stop')
        if stop:
            method = 'privateDeleteStopOrderCancel'
        return getattr(self, method)(self.extend(request, params))

    def fetch_orders_by_status(self, status, symbol=None, since=None, limit=None, params={}):
        """
        fetch a list of orders
        :param str status: *not used for stop orders* 'open' or 'closed'
        :param str|None symbol: unified market symbol
        :param int|None since: timestamp in ms of the earliest order
        :param int|None limit: max number of orders to return
        :param dict params: exchange specific params
        :param int|None params['until']: end time in ms
        :param bool|None params['stop']: True if fetching stop orders
        :param str|None params['side']: buy or sell
        :param str|None params['type']: limit, market, limit_stop or market_stop
        :param str|None params['tradeType']: TRADE for spot trading, MARGIN_TRADE for Margin Trading
        :param int|None params['currentPage']: *stop orders only* current page
        :param str|None params['orderIds']: *stop orders only* comma seperated order ID list
        :returns: An `array of order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        lowercaseStatus = status.lower()
        if lowercaseStatus == 'open':
            lowercaseStatus = 'active'
        elif lowercaseStatus == 'closed':
            lowercaseStatus = 'done'
        request = {'status': lowercaseStatus}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['startAt'] = since
        if limit is not None:
            request['pageSize'] = limit
        until = self.safe_integer_2(params, 'until', 'till')
        if until:
            request['endAt'] = until
        stop = self.safe_value(params, 'stop')
        params = self.omit(params, ['stop', 'till', 'until'])
        method = 'privateGetOrders'
        if stop:
            method = 'privateGetStopOrder'
        response = getattr(self, method)(self.extend(request, params))
        responseData = self.safe_value(response, 'data', {})
        orders = self.safe_value(responseData, 'items', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param int|None params['till']: end time in ms
        :param str|None params['side']: buy or sell
        :param str|None params['type']: limit, market, limit_stop or market_stop
        :param str|None params['tradeType']: TRADE for spot trading, MARGIN_TRADE for Margin Trading
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        return self.fetch_orders_by_status('done', symbol, since, limit, params)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param int params['till']: end time in ms
        :param bool params['stop']: True if fetching stop orders
        :param str params['side']: buy or sell
        :param str params['type']: limit, market, limit_stop or market_stop
        :param str params['tradeType']: TRADE for spot trading, MARGIN_TRADE for Margin Trading
        :param int params['currentPage']: *stop orders only* current page
        :param str params['orderIds']: *stop orders only* comma seperated order ID list
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        return self.fetch_orders_by_status('active', symbol, since, limit, params)

    def fetch_order(self, id, symbol=None, params={}):
        """
        fetch an order
        :param str id: Order id
        :param str symbol: not sent to exchange except for stop orders with clientOid, but used internally by CCXT to filter
        :param dict params: exchange specific parameters
        :param bool params['stop']: True if fetching a stop order
        :param bool params['clientOid']: unique order id created by users to identify their orders
        :returns: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        self.load_markets()
        request = {}
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
        stop = self.safe_value(params, 'stop')
        market = None
        if symbol is not None:
            market = self.market(symbol)
        params = self.omit(params, 'stop')
        method = 'privateGetOrdersOrderId'
        if clientOrderId is not None:
            request['clientOid'] = clientOrderId
            if stop:
                method = 'privateGetStopOrderQueryOrderByClientOid'
                if symbol is not None:
                    request['symbol'] = market['id']
            else:
                method = 'privateGetOrderClientOrderClientOid'
        else:
            if id is None:
                raise InvalidOrder(self.id + ' fetchOrder() requires an order id')
            if stop:
                method = 'privateGetStopOrderOrderId'
            request['orderId'] = id
        params = self.omit(params, ['clientOid', 'clientOrderId'])
        response = getattr(self, method)(self.extend(request, params))
        responseData = self.safe_value(response, 'data')
        if method == 'privateGetStopOrderQueryOrderByClientOid':
            responseData = self.safe_value(responseData, 0)
        return self.parse_order(responseData, market)

    def parse_order(self, order, market=None):
        marketId = self.safe_string(order, 'symbol')
        symbol = self.safe_symbol(marketId, market, '-')
        orderId = self.safe_string(order, 'id')
        type = self.safe_string(order, 'type')
        timestamp = self.safe_integer(order, 'createdAt')
        datetime = self.iso8601(timestamp)
        price = self.safe_string(order, 'price')
        side = self.safe_string(order, 'side')
        feeCurrencyId = self.safe_string(order, 'feeCurrency')
        feeCurrency = self.safe_currency_code(feeCurrencyId)
        feeCost = self.safe_number(order, 'fee')
        amount = self.safe_string(order, 'size')
        filled = self.safe_string(order, 'dealSize')
        cost = self.safe_string(order, 'dealFunds')
        isActive = self.safe_value(order, 'isActive', False)
        cancelExist = self.safe_value(order, 'cancelExist', False)
        stop = self.safe_string(order, 'stop')
        stopTriggered = self.safe_value(order, 'stopTriggered', False)
        status = 'open' if isActive else 'closed'
        cancelExistWithStop = cancelExist or (not isActive and stop and (not stopTriggered))
        status = 'canceled' if cancelExistWithStop else status
        fee = {'currency': feeCurrency, 'cost': feeCost}
        clientOrderId = self.safe_string(order, 'clientOid')
        timeInForce = self.safe_string(order, 'timeInForce')
        stopPrice = self.safe_number(order, 'stopPrice')
        postOnly = self.safe_value(order, 'postOnly')
        return self.safe_order({'id': orderId, 'clientOrderId': clientOrderId, 'symbol': symbol, 'type': type, 'timeInForce': timeInForce, 'postOnly': postOnly, 'side': side, 'amount': amount, 'price': price, 'stopPrice': stopPrice, 'triggerPrice': stopPrice, 'cost': cost, 'filled': filled, 'remaining': None, 'timestamp': timestamp, 'datetime': datetime, 'fee': fee, 'status': status, 'info': order, 'lastTradeTimestamp': None, 'average': None, 'trades': None}, market)

    def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        """
        fetch all the trades made from a single order
        :param str id: order id
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        request = {'orderId': id}
        return self.fetch_my_trades(symbol, since, limit, self.extend(request, params))

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if limit is not None:
            request['pageSize'] = limit
        method = self.options['fetchMyTradesMethod']
        parseResponseData = False
        if method == 'private_get_fills':
            if since is not None:
                request['startAt'] = since
        elif method == 'private_get_limit_fills':
            parseResponseData = True
        elif method == 'private_get_hist_orders':
            if since is not None:
                request['startAt'] = int(since / 1000)
        else:
            raise ExchangeError(self.id + ' fetchMyTradesMethod() invalid method')
        response = getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        trades = None
        if parseResponseData:
            trades = data
        else:
            trades = self.safe_value(data, 'items', [])
        return self.parse_trades(trades, market, since, limit)

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'symbol': market['id']}
        response = self.publicGetMarketHistories(self.extend(request, params))
        trades = self.safe_value(response, 'data', [])
        return self.parse_trades(trades, market, since, limit)

    def parse_trade(self, trade, market=None):
        marketId = self.safe_string(trade, 'symbol')
        market = self.safe_market(marketId, market, '-')
        id = self.safe_string_2(trade, 'tradeId', 'id')
        orderId = self.safe_string(trade, 'orderId')
        takerOrMaker = self.safe_string(trade, 'liquidity')
        timestamp = self.safe_integer(trade, 'time')
        if timestamp is not None:
            timestamp = int(timestamp / 1000000)
        else:
            timestamp = self.safe_integer(trade, 'createdAt')
            if 'dealValue' in trade and timestamp is not None:
                timestamp = timestamp * 1000
        priceString = self.safe_string_2(trade, 'price', 'dealPrice')
        amountString = self.safe_string_2(trade, 'size', 'amount')
        side = self.safe_string(trade, 'side')
        fee = None
        feeCostString = self.safe_string(trade, 'fee')
        if feeCostString is not None:
            feeCurrencyId = self.safe_string(trade, 'feeCurrency')
            feeCurrency = self.safe_currency_code(feeCurrencyId)
            if feeCurrency is None:
                feeCurrency = market['quote'] if side == 'sell' else market['base']
            fee = {'cost': feeCostString, 'currency': feeCurrency, 'rate': self.safe_string(trade, 'feeRate')}
        type = self.safe_string(trade, 'type')
        if type == 'match':
            type = None
        costString = self.safe_string_2(trade, 'funds', 'dealValue')
        return self.safe_trade({'info': trade, 'id': id, 'order': orderId, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': market['symbol'], 'type': type, 'takerOrMaker': takerOrMaker, 'side': side, 'price': priceString, 'amount': amountString, 'cost': costString, 'fee': fee}, market)

    def fetch_trading_fee(self, symbol, params={}):
        """
        fetch the trading fees for a market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request = {'symbols': market['id']}
        response = self.privateGetTradeFees(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        first = self.safe_value(data, 0)
        marketId = self.safe_string(first, 'symbol')
        return {'info': response, 'symbol': self.safe_symbol(marketId, market), 'maker': self.safe_number(first, 'makerFeeRate'), 'taker': self.safe_number(first, 'takerFeeRate'), 'percentage': True, 'tierBased': True}

    def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        (tag, params) = self.handle_withdraw_tag_and_params(tag, params)
        self.load_markets()
        self.check_address(address)
        currency = self.currency(code)
        request = {'currency': currency['id'], 'address': address, 'amount': amount}
        if tag is not None:
            request['memo'] = tag
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper(params, 'network')
        network = self.safe_string_lower(networks, network, network)
        if network is not None:
            network = network.lower()
            request['chain'] = network
            params = self.omit(params, 'network')
        response = self.privatePostWithdrawals(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_transaction(data, currency)

    def parse_transaction_status(self, status):
        statuses = {'SUCCESS': 'ok', 'PROCESSING': 'ok', 'FAILURE': 'failed'}
        return self.safe_string(statuses, status)

    def parse_transaction(self, transaction, currency=None):
        currencyId = self.safe_string(transaction, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        address = self.safe_string(transaction, 'address')
        amount = self.safe_string(transaction, 'amount')
        txid = self.safe_string(transaction, 'walletTxId')
        if txid is not None:
            txidParts = txid.split('@')
            numTxidParts = len(txidParts)
            if numTxidParts > 1:
                if address is None:
                    if len(txidParts[1]) > 1:
                        address = txidParts[1]
            txid = txidParts[0]
        type = 'withdrawal' if txid is None else 'deposit'
        rawStatus = self.safe_string(transaction, 'status')
        fee = None
        feeCost = self.safe_string(transaction, 'fee')
        if feeCost is not None:
            rate = None
            if amount is not None:
                rate = Precise.string_div(feeCost, amount)
            fee = {'cost': self.parse_number(feeCost), 'rate': self.parse_number(rate), 'currency': code}
        timestamp = self.safe_integer_2(transaction, 'createdAt', 'createAt')
        updated = self.safe_integer(transaction, 'updatedAt')
        isV1 = not 'createdAt' in transaction
        if isV1:
            type = 'withdrawal' if 'address' in transaction else 'deposit'
            if timestamp is not None:
                timestamp = timestamp * 1000
            if updated is not None:
                updated = updated * 1000
        tag = self.safe_string(transaction, 'memo')
        network = self.safe_string(transaction, 'chain')
        return {'info': transaction, 'id': self.safe_string_2(transaction, 'id', 'withdrawalId'), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'network': network, 'address': address, 'addressTo': address, 'addressFrom': None, 'tag': tag, 'tagTo': tag, 'tagFrom': None, 'currency': code, 'amount': self.parse_number(amount), 'txid': txid, 'type': type, 'status': self.parse_transaction_status(rawStatus), 'comment': self.safe_string(transaction, 'remark'), 'fee': fee, 'updated': updated}

    def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if limit is not None:
            request['pageSize'] = limit
        method = 'privateGetDeposits'
        if since is not None:
            if since < 1550448000000:
                request['startAt'] = int(since / 1000)
                method = 'privateGetHistDeposits'
            else:
                request['startAt'] = since
        response = getattr(self, method)(self.extend(request, params))
        responseData = response['data']['items']
        return self.parse_transactions(responseData, currency, since, limit, {'type': 'deposit'})

    def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        self.load_markets()
        request = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if limit is not None:
            request['pageSize'] = limit
        method = 'privateGetWithdrawals'
        if since is not None:
            if since < 1550448000000:
                request['startAt'] = int(since / 1000)
                method = 'privateGetHistWithdrawals'
            else:
                request['startAt'] = since
        response = getattr(self, method)(self.extend(request, params))
        responseData = response['data']['items']
        return self.parse_transactions(responseData, currency, since, limit, {'type': 'withdrawal'})

    def parse_balance_helper(self, entry):
        account = self.account()
        account['used'] = self.safe_string(entry, 'holdBalance')
        account['free'] = self.safe_string(entry, 'availableBalance')
        account['total'] = self.safe_string(entry, 'totalBalance')
        debt = self.safe_string(entry, 'liability')
        interest = self.safe_string(entry, 'interest')
        account['debt'] = Precise.string_add(debt, interest)
        return account

    def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        see https://docs.kucoin.com/#list-accounts
        see https://docs.kucoin.com/#query-isolated-margin-account-info
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param dict params['marginMode']: 'cross' or 'isolated', margin type for fetching margin balance
        :param dict params['type']: extra parameters specific to the kucoin api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        self.load_markets()
        code = self.safe_string(params, 'code')
        currency = None
        if code is not None:
            currency = self.currency(code)
        defaultType = self.safe_string_2(self.options, 'fetchBalance', 'defaultType', 'spot')
        requestedType = self.safe_string(params, 'type', defaultType)
        accountsByType = self.safe_value(self.options, 'accountsByType')
        type = self.safe_string(accountsByType, requestedType, requestedType)
        params = self.omit(params, 'type')
        (marginMode, query) = self.handle_margin_mode_and_params('fetchBalance', params)
        method = 'privateGetAccounts'
        request = {}
        isolated = marginMode == 'isolated' or type == 'isolated'
        cross = marginMode == 'cross' or type == 'cross'
        if isolated:
            method = 'privateGetIsolatedAccounts'
            if currency is not None:
                request['balanceCurrency'] = currency['id']
        elif cross:
            method = 'privateGetMarginAccount'
        else:
            if currency is not None:
                request['currency'] = currency['id']
            request['type'] = type
        response = getattr(self, method)(self.extend(request, query))
        data = self.safe_value(response, 'data', [])
        result = {'info': response, 'timestamp': None, 'datetime': None}
        if isolated:
            assets = self.safe_value(data, 'assets', [])
            for i in range(0, len(assets)):
                entry = assets[i]
                marketId = self.safe_string(entry, 'symbol')
                symbol = self.safe_symbol(marketId, None, '_')
                base = self.safe_value(entry, 'baseAsset', {})
                quote = self.safe_value(entry, 'quoteAsset', {})
                baseCode = self.safe_currency_code(self.safe_string(base, 'currency'))
                quoteCode = self.safe_currency_code(self.safe_string(quote, 'currency'))
                subResult = {}
                subResult[baseCode] = self.parse_balance_helper(base)
                subResult[quoteCode] = self.parse_balance_helper(quote)
                result[symbol] = self.safe_balance(subResult)
        elif cross:
            accounts = self.safe_value(data, 'accounts', [])
            for i in range(0, len(accounts)):
                balance = accounts[i]
                currencyId = self.safe_string(balance, 'currency')
                code = self.safe_currency_code(currencyId)
                result[code] = self.parse_balance_helper(balance)
        else:
            for i in range(0, len(data)):
                balance = data[i]
                balanceType = self.safe_string(balance, 'type')
                if balanceType == type:
                    currencyId = self.safe_string(balance, 'currency')
                    code = self.safe_currency_code(currencyId)
                    account = self.account()
                    account['total'] = self.safe_string(balance, 'balance')
                    account['free'] = self.safe_string(balance, 'available')
                    account['used'] = self.safe_string(balance, 'holds')
                    result[code] = account
        return result if isolated else self.safe_balance(result)

    def transfer(self, code, amount, fromAccount, toAccount, params={}):
        """
        transfer currency internally between wallets on the same account
        see https://docs.kucoin.com/#inner-transfer
        see https://docs.kucoin.com/futures/#transfer-funds-to-kucoin-main-account-2
        :param str code: unified currency code
        :param float amount: amount to transfer
        :param str fromAccount: account to transfer from
        :param str toAccount: account to transfer to
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `transfer structure <https://docs.ccxt.com/en/latest/manual.html#transfer-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        requestedAmount = self.currency_to_precision(code, amount)
        fromId = self.convert_type_to_account(fromAccount)
        toId = self.convert_type_to_account(toAccount)
        fromIsolated = self.in_array(fromId, self.ids)
        toIsolated = self.in_array(toId, self.ids)
        if fromId == 'contract':
            if toId != 'main':
                raise ExchangeError(self.id + ' transfer() only supports transferring from futures account to main account')
            request = {'currency': currency['id'], 'amount': requestedAmount}
            if not 'bizNo' in params:
                request['bizNo'] = self.uuid22()
            response = self.futuresPrivatePostTransferOut(self.extend(request, params))
            data = self.safe_value(response, 'data')
            return self.parse_transfer(data, currency)
        else:
            request = {'currency': currency['id'], 'amount': requestedAmount}
            if fromIsolated or toIsolated:
                if self.in_array(fromId, self.ids):
                    request['fromTag'] = fromId
                    fromId = 'isolated'
                if self.in_array(toId, self.ids):
                    request['toTag'] = toId
                    toId = 'isolated'
            request['from'] = fromId
            request['to'] = toId
            if not 'clientOid' in params:
                request['clientOid'] = self.uuid()
            response = self.privatePostAccountsInnerTransfer(self.extend(request, params))
            data = self.safe_value(response, 'data')
            return self.parse_transfer(data, currency)

    def parse_transfer(self, transfer, currency=None):
        timestamp = self.safe_integer(transfer, 'createdAt')
        currencyId = self.safe_string(transfer, 'currency')
        rawStatus = self.safe_string(transfer, 'status')
        accountFromRaw = self.safe_string_lower(transfer, 'payAccountType')
        accountToRaw = self.safe_string_lower(transfer, 'recAccountType')
        accountsByType = self.safe_value(self.options, 'accountsByType')
        accountFrom = self.safe_string(accountsByType, accountFromRaw, accountFromRaw)
        accountTo = self.safe_string(accountsByType, accountToRaw, accountToRaw)
        return {'id': self.safe_string_2(transfer, 'applyId', 'orderId'), 'currency': self.safe_currency_code(currencyId, currency), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'amount': self.safe_number(transfer, 'amount'), 'fromAccount': accountFrom, 'toAccount': accountTo, 'status': self.parse_transfer_status(rawStatus), 'info': transfer}

    def parse_transfer_status(self, status):
        statuses = {'PROCESSING': 'pending'}
        return self.safe_string(statuses, status, status)

    def parse_ledger_entry_type(self, type):
        types = {'Assets Transferred in After Upgrading': 'transfer', 'Deposit': 'transaction', 'Withdrawal': 'transaction', 'Transfer': 'transfer', 'Trade_Exchange': 'trade', 'KuCoin Bonus': 'bonus', 'Referral Bonus': 'referral', 'Rewards': 'bonus', 'Airdrop/Fork': 'airdrop', 'Other rewards': 'bonus', 'Fee Rebate': 'rebate', 'Buy Crypto': 'trade', 'Sell Crypto': 'sell', 'Public Offering Purchase': 'trade', 'Refunded Fees': 'fee', 'KCS Pay Fees': 'fee', 'Margin Trade': 'trade', 'Loans': 'Loans', 'Instant Exchange': 'trade', 'Sub-account transfer': 'transfer', 'Liquidation Fees': 'fee'}
        return self.safe_string(types, type, type)

    def parse_ledger_entry(self, item, currency=None):
        id = self.safe_string(item, 'id')
        currencyId = self.safe_string(item, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        amount = self.safe_number(item, 'amount')
        balanceAfter = None
        bizType = self.safe_string(item, 'bizType')
        type = self.parse_ledger_entry_type(bizType)
        direction = self.safe_string(item, 'direction')
        timestamp = self.safe_integer(item, 'createdAt')
        datetime = self.iso8601(timestamp)
        account = self.safe_string(item, 'accountType')
        context = self.safe_string(item, 'context')
        referenceId = None
        if context is not None and context != '':
            try:
                parsed = json.loads(context)
                orderId = self.safe_string(parsed, 'orderId')
                tradeId = self.safe_string(parsed, 'tradeId')
                if tradeId is not None:
                    referenceId = tradeId
                else:
                    referenceId = orderId
            except Exception as exc:
                referenceId = context
        fee = None
        feeCost = self.safe_number(item, 'fee')
        feeCurrency = None
        if feeCost != 0:
            feeCurrency = code
            fee = {'cost': feeCost, 'currency': feeCurrency}
        return {'id': id, 'direction': direction, 'account': account, 'referenceId': referenceId, 'referenceAccount': account, 'type': type, 'currency': code, 'amount': amount, 'timestamp': timestamp, 'datetime': datetime, 'before': None, 'after': balanceAfter, 'status': None, 'fee': fee, 'info': item}

    def fetch_ledger(self, code=None, since=None, limit=None, params={}):
        """
        fetch the history of changes, actions done by the user or operations that altered balance of the user
        :param str|None code: unified currency code, default is None
        :param int|None since: timestamp in ms of the earliest ledger entry, default is None
        :param int|None limit: max number of ledger entrys to return, default is None
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns dict: a `ledger structure <https://docs.ccxt.com/en/latest/manual.html#ledger-structure>`
        """
        self.load_markets()
        self.load_accounts()
        request = {}
        if since is not None:
            request['startAt'] = since
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = self.privateGetAccountsLedgers(self.extend(request, params))
        data = self.safe_value(response, 'data')
        items = self.safe_value(data, 'items')
        return self.parse_ledger(items, currency, since, limit)

    def calculate_rate_limiter_cost(self, api, method, path, params, config={}, context={}):
        versions = self.safe_value(self.options, 'versions', {})
        apiVersions = self.safe_value(versions, api, {})
        methodVersions = self.safe_value(apiVersions, method, {})
        defaultVersion = self.safe_string(methodVersions, path, self.options['version'])
        version = self.safe_string(params, 'version', defaultVersion)
        if version == 'v3' and 'v3' in config:
            return config['v3']
        elif version == 'v2' and 'v2' in config:
            return config['v2']
        elif version == 'v1' and 'v1' in config:
            return config['v1']
        return self.safe_value(config, 'cost', 1)

    def fetch_borrow_rate_history(self, code, since=None, limit=None, params={}):
        """
        retrieves a history of a currencies borrow interest rate at specific time slots
        see https://docs.kucoin.com/#margin-trade-data
        :param str code: unified currency code
        :param int|None since: timestamp for the earliest borrow rate
        :param int|None limit: the maximum number of [borrow rate structures]
        :param dict params: extra parameters specific to the kucoin api endpoint
        :returns [dict]: an array of `borrow rate structures <https://docs.ccxt.com/en/latest/manual.html#borrow-rate-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        response = self.privateGetMarginTradeLast(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_borrow_rate_history(data, code)

    def parse_borrow_rate_history(self, response, code, since, limit):
        result = []
        for i in range(0, len(response)):
            item = response[i]
            borrowRate = self.parse_borrow_rate(item)
            result.append(borrowRate)
        sorted = self.sort_by(result, 'timestamp')
        return self.filter_by_currency_since_limit(sorted, code, since, limit)

    def parse_borrow_rate(self, info, currency=None):
        timestampId = self.safe_string(info, 'timestamp')
        timestamp = Precise.string_mul(timestampId, '0.000001')
        currencyId = self.safe_string(info, 'currency')
        return {'currency': self.safe_currency_code(currencyId, currency), 'rate': self.safe_number(info, 'dailyIntRate'), 'period': 86400000, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': info}

    def fetch_borrow_interest(self, code=None, symbol=None, since=None, limit=None, params={}):
        """
        fetch the interest owed by the user for borrowing currency for margin trading
        see https://docs.kucoin.com/#get-repay-record
        see https://docs.kucoin.com/#query-isolated-margin-account-info
        :param str|None code: unified currency code
        :param str|None symbol: unified market symbol, required for isolated margin
        :param int|None since: the earliest time in ms to fetch borrrow interest for
        :param int|None limit: the maximum number of structures to retrieve
        :param dict params: extra parameters specific to the kucoin api endpoint
        :param str|None params['marginMode']: 'cross' or 'isolated' default is 'cross'
        :returns [dict]: a list of `borrow interest structures <https://docs.ccxt.com/en/latest/manual.html#borrow-interest-structure>`
        """
        self.load_markets()
        marginMode = None
        (marginMode, params) = self.handle_margin_mode_and_params('fetchBorrowInterest', params)
        if marginMode is None:
            marginMode = 'cross'
        request = {}
        method = 'privateGetMarginBorrowOutstanding'
        if marginMode == 'isolated':
            if code is not None:
                currency = self.currency(code)
                request['balanceCurrency'] = currency['id']
            method = 'privateGetIsolatedAccounts'
        elif code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        response = getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        assets = self.safe_value(data, 'assets', []) if marginMode == 'isolated' else self.safe_value(data, 'items', [])
        return self.parse_borrow_interests(assets, None)

    def parse_borrow_interest(self, info, market=None):
        marketId = self.safe_string(info, 'symbol')
        marginMode = 'cross' if marketId is None else 'isolated'
        market = self.safe_market(marketId, market)
        symbol = self.safe_string(market, 'symbol')
        timestamp = self.safe_integer(info, 'createdAt')
        isolatedBase = self.safe_value(info, 'baseAsset', {})
        amountBorrowed = None
        interest = None
        currencyId = None
        if marginMode == 'isolated':
            amountBorrowed = self.safe_number(isolatedBase, 'liability')
            interest = self.safe_number(isolatedBase, 'interest')
            currencyId = self.safe_string(isolatedBase, 'currency')
        else:
            amountBorrowed = self.safe_number(info, 'principal')
            interest = self.safe_number(info, 'accruedInterest')
            currencyId = self.safe_string(info, 'currency')
        return {'symbol': symbol, 'marginMode': marginMode, 'currency': self.safe_currency_code(currencyId), 'interest': interest, 'interestRate': self.safe_number(info, 'dailyIntRate'), 'amountBorrowed': amountBorrowed, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': info}

    def borrow_margin(self, code, amount, symbol=None, params={}):
        """
        create a loan to borrow margin
        see https://docs.kucoin.com/#post-borrow-order
        see https://docs.kucoin.com/#isolated-margin-borrowing
        :param str code: unified currency code of the currency to borrow
        :param float amount: the amount to borrow
        :param str|None symbol: unified market symbol, required for isolated margin
        :param dict params: extra parameters specific to the kucoin api endpoints
        :param str params['timeInForce']: either IOC or FOK
        :param str|None params['marginMode']: 'cross' or 'isolated' default is 'cross'
        :returns dict: a `margin loan structure <https://docs.ccxt.com/en/latest/manual.html#margin-loan-structure>`
        """
        marginMode = self.safe_string(params, 'marginMode')
        params = self.omit(params, 'marginMode')
        self.check_required_margin_argument('borrowMargin', symbol, marginMode)
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id'], 'size': self.currency_to_precision(code, amount)}
        method = None
        timeInForce = self.safe_string_n(params, ['timeInForce', 'type', 'borrowStrategy'], 'IOC')
        timeInForceRequest = None
        if symbol is None:
            method = 'privatePostMarginBorrow'
            timeInForceRequest = 'type'
        else:
            market = self.market(symbol)
            request['symbol'] = market['id']
            timeInForceRequest = 'borrowStrategy'
            method = 'privatePostIsolatedBorrow'
        request[timeInForceRequest] = timeInForce
        params = self.omit(params, ['timeInForce', 'type', 'borrowStrategy'])
        response = getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_margin_loan(data, currency)

    def repay_margin(self, code, amount, symbol=None, params={}):
        """
        repay borrowed margin and interest
        see https://docs.kucoin.com/#one-click-repayment
        see https://docs.kucoin.com/#quick-repayment
        :param str code: unified currency code of the currency to repay
        :param float amount: the amount to repay
        :param str|None symbol: unified market symbol
        :param dict params: extra parameters specific to the kucoin api endpoints
        :param str|None params['sequence']: cross margin repay sequence, either 'RECENTLY_EXPIRE_FIRST' or 'HIGHEST_RATE_FIRST' default is 'RECENTLY_EXPIRE_FIRST'
        :param str|None params['seqStrategy']: isolated margin repay sequence, either 'RECENTLY_EXPIRE_FIRST' or 'HIGHEST_RATE_FIRST' default is 'RECENTLY_EXPIRE_FIRST'
        :param str|None params['marginMode']: 'cross' or 'isolated' default is 'cross'
        :returns dict: a `margin loan structure <https://docs.ccxt.com/en/latest/manual.html#margin-loan-structure>`
        """
        marginMode = self.safe_string(params, 'marginMode')
        params = self.omit(params, 'marginMode')
        self.check_required_margin_argument('repayMargin', symbol, marginMode)
        self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id'], 'size': self.currency_to_precision(code, amount)}
        method = None
        sequence = self.safe_string_2(params, 'sequence', 'seqStrategy', 'RECENTLY_EXPIRE_FIRST')
        sequenceRequest = None
        if symbol is None:
            method = 'privatePostMarginRepayAll'
            sequenceRequest = 'sequence'
        else:
            market = self.market(symbol)
            request['symbol'] = market['id']
            sequenceRequest = 'seqStrategy'
            method = 'privatePostIsolatedRepayAll'
        request[sequenceRequest] = sequence
        params = self.omit(params, ['sequence', 'seqStrategy'])
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_margin_loan(response, currency)

    def parse_margin_loan(self, info, currency=None):
        timestamp = self.milliseconds()
        currencyId = self.safe_string(info, 'currency')
        return {'id': self.safe_string(info, 'orderId'), 'currency': self.safe_currency_code(currencyId, currency), 'amount': self.safe_number(info, 'actualSize'), 'symbol': None, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': info}

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        versions = self.safe_value(self.options, 'versions', {})
        apiVersions = self.safe_value(versions, api, {})
        methodVersions = self.safe_value(apiVersions, method, {})
        defaultVersion = self.safe_string(methodVersions, path, self.options['version'])
        version = self.safe_string(params, 'version', defaultVersion)
        params = self.omit(params, 'version')
        endpoint = '/api/' + version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        endpart = ''
        headers = headers if headers is not None else {}
        url = self.urls['api'][api]
        isSandbox = url.find('sandbox') >= 0
        if path == 'symbols' and (not isSandbox):
            endpoint = '/api/v2/' + self.implode_params(path, params)
        if query:
            if method == 'GET' or method == 'DELETE':
                endpoint += '?' + self.rawencode(query)
            else:
                body = self.json(query)
                endpart = body
                headers['Content-Type'] = 'application/json'
        url = url + endpoint
        isFuturePrivate = api == 'futuresPrivate'
        isPrivate = api == 'private'
        if isPrivate or isFuturePrivate:
            self.check_required_credentials()
            timestamp = str(self.nonce())
            headers = self.extend({'KC-API-KEY-VERSION': '2', 'KC-API-KEY': self.apiKey, 'KC-API-TIMESTAMP': timestamp}, headers)
            apiKeyVersion = self.safe_string(headers, 'KC-API-KEY-VERSION')
            if apiKeyVersion == '2':
                passphrase = self.hmac(self.encode(self.password), self.encode(self.secret), hashlib.sha256, 'base64')
                headers['KC-API-PASSPHRASE'] = passphrase
            else:
                headers['KC-API-PASSPHRASE'] = self.password
            payload = timestamp + method + endpoint + endpart
            signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
            headers['KC-API-SIGN'] = signature
            partner = self.safe_value(self.options, 'partner', {})
            partner = self.safe_value(partner, 'future', partner) if isFuturePrivate else self.safe_value(partner, 'spot', partner)
            partnerId = self.safe_string(partner, 'id')
            partnerSecret = self.safe_string_2(partner, 'secret', 'key')
            if partnerId is not None and partnerSecret is not None:
                partnerPayload = timestamp + partnerId + self.apiKey
                partnerSignature = self.hmac(self.encode(partnerPayload), self.encode(partnerSecret), hashlib.sha256, 'base64')
                headers['KC-API-PARTNER-SIGN'] = partnerSignature
                headers['KC-API-PARTNER'] = partnerId
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            self.throw_broadly_matched_exception(self.exceptions['broad'], body, body)
            return
        errorCode = self.safe_string(response, 'code')
        message = self.safe_string(response, 'msg', '')
        feedback = self.id + ' ' + message
        self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
        self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
        self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)