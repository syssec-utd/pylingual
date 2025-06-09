import urllib.parse
from binance_f.constant.system import WebSocketDefine
from binance_f.impl.websocketrequestimpl import WebsocketRequestImpl
from binance_f.impl.websocketconnection import WebsocketConnection
from binance_f.impl.websocketwatchdog import WebSocketWatchDog
from binance_f.impl.restapirequestimpl import RestApiRequestImpl
from binance_f.model import *
from binance_f.model.constant import *
from binance_f.base.printobject import *

class SubscriptionClient(object):

    def __init__(self, **kwargs):
        """
        Create the subscription client to subscribe the update from server.

        :param kwargs: The option of subscription connection.
            api_key: The public key applied from Binance.
            secret_key: The private key applied from Binance.
            uri: Set the URI for subscription.
            is_auto_connect: When the connection lost is happening on the subscription line, specify whether the client
                            reconnect to server automatically. The connection lost means:
                                Caused by network problem
                                The connection close triggered by server (happened every 24 hours)
                            No any message can be received from server within a specified time, see receive_limit_ms
            receive_limit_ms: Set the receive limit in millisecond. If no message is received within this limit time,
                            the connection will be disconnected.
            connection_delay_failure: If auto reconnect is enabled, specify the delay time before reconnect.
        """
        api_key = None
        secret_key = None
        if 'api_key' in kwargs:
            api_key = kwargs['api_key']
        if 'secret_key' in kwargs:
            secret_key = kwargs['secret_key']
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.websocket_request_impl = WebsocketRequestImpl(self.__api_key)
        self.connections = list()
        self.uri = WebSocketDefine.Uri
        is_auto_connect = True
        receive_limit_ms = 60000
        connection_delay_failure = 1
        if 'uri' in kwargs:
            self.uri = kwargs['uri']
        if 'is_auto_connect' in kwargs:
            is_auto_connect = kwargs['is_auto_connect']
        if 'receive_limit_ms' in kwargs:
            receive_limit_ms = kwargs['receive_limit_ms']
        if 'connection_delay_failure' in kwargs:
            connection_delay_failure = kwargs['connection_delay_failure']
        self.__watch_dog = WebSocketWatchDog(is_auto_connect, receive_limit_ms, connection_delay_failure)

    def __create_connection(self, request):
        connection = WebsocketConnection(self.__api_key, self.__secret_key, self.uri, self.__watch_dog, request)
        self.connections.append(connection)
        connection.connect()

    def unsubscribe_all(self):
        for conn in self.connections:
            conn.close()
        self.connections.clear()

    def subscribe_aggregate_trade_event(self, symbol: 'str', callback, error_handler=None):
        """
        Aggregate Trade Streams

        The Aggregate Trade Streams push trade information that is aggregated for a single taker order every 100 milliseconds.

        Stream Name: <symbol>@aggTrade
        """
        request = self.websocket_request_impl.subscribe_aggregate_trade_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_mark_price_event(self, symbol: 'str', callback, error_handler=None):
        """
        Mark Price Stream

        Mark price for a single symbol pushed every 3 secends.

        Stream Name: <symbol>@markPrice
        """
        request = self.websocket_request_impl.subscribe_mark_price_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_continuous_candlestick_event(self, pair: 'str', contract_type: 'ContractType', interval: 'CandlestickInterval', callback, error_handler=None):
        """
        Continuous Kline/Candlestick Streams

        The continuous Kline/Candlestick Stream push updates to the current klines/candlestick every 250 milliseconds (if existing).

        Stream Name: <pair><contractType>@continuousKline_<interval>
        """
        request = self.websocket_request_impl.subscribe_continuous_candlestick_event(pair, contract_type, interval, callback, error_handler)
        self.__create_connection(request)

    def subscribe_candlestick_event(self, symbol: 'str', interval: 'CandlestickInterval', callback, error_handler=None):
        """
        Kline/Candlestick Streams

        The Kline/Candlestick Stream push updates to the current klines/candlestick every 250 milliseconds (if existing).

        Stream Name: <symbol>@kline_<interval>
        """
        request = self.websocket_request_impl.subscribe_candlestick_event(symbol, interval, callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_miniticker_event(self, symbol: 'str', callback, error_handler=None):
        """
        Individual Symbol Mini Ticker Stream

        24hr rolling window mini-ticker statistics for a single symbol pushed every 3 seconds. These are NOT the statistics of the UTC day, 
        but a 24hr rolling window from requestTime to 24hrs before.

        Stream Name: <symbol>@miniTicker
        """
        request = self.websocket_request_impl.subscribe_symbol_miniticker_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_miniticker_event(self, callback, error_handler=None):
        """
        All Market Mini Tickers Stream

        24hr rolling window mini-ticker statistics for all symbols pushed every 3 seconds. 
        These are NOT the statistics of the UTC day, but a 24hr rolling window from requestTime to 24hrs before. 
        Note that only tickers that have changed will be present in the array.

        Stream Name: !miniTicker@arr
        """
        request = self.websocket_request_impl.subscribe_all_miniticker_event(callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_ticker_event(self, symbol: 'str', callback, error_handler=None):
        """
        Individual Symbol Ticker Streams

        24hr rollwing window ticker statistics for a single symbol pushed every 3 seconds. These are NOT the statistics of the UTC day, 
        but a 24hr rolling window from requestTime to 24hrs before.

        Stream Name: <symbol>@ticker
        """
        request = self.websocket_request_impl.subscribe_symbol_ticker_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_ticker_event(self, callback, error_handler=None):
        """
        All Market Tickers Stream

        24hr rollwing window ticker statistics for all symbols pushed every 3 seconds. These are NOT the statistics of the UTC day, but a 24hr rolling window from requestTime to 24hrs before. 
        Note that only tickers that have changed will be present in the array.

        Stream Name: !ticker@arr
        """
        request = self.websocket_request_impl.subscribe_all_ticker_event(callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_bookticker_event(self, symbol: 'str', callback, error_handler=None):
        """
        Individual Symbol Book Ticker Streams

        Pushes any update to the best bid or ask's price or quantity in real-time for a specified symbol.

        Stream Name: <symbol>@bookTicker
        """
        request = self.websocket_request_impl.subscribe_symbol_bookticker_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_bookticker_event(self, callback, error_handler=None):
        """
        All Book Tickers Stream

        Pushes any update to the best bid or ask's price or quantity in real-time for all symbols.

        Stream Name: !bookTicker
        """
        request = self.websocket_request_impl.subscribe_all_bookticker_event(callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_liquidation_event(self, symbol: 'str', callback, error_handler=None):
        """
        Liquidation Order Streams

        The Liquidation Order Streams push force liquidation order information for specific symbol

        Stream Name:  <symbol>@forceOrder
        """
        request = self.websocket_request_impl.subscribe_symbol_liquidation_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_liquidation_event(self, callback, error_handler=None):
        """
        All Market Liquidation Order Streams

        The All Liquidation Order Streams push force liquidation order information for all symbols in the market.

        Stream Name: !forceOrder@arr
        """
        request = self.websocket_request_impl.subscribe_all_liquidation_event(callback, error_handler)
        self.__create_connection(request)

    def subscribe_book_depth_event(self, symbol: 'str', limit: 'int', callback, error_handler=None, update_time: 'UpdateTime'=UpdateTime.INVALID):
        """
        Partial Book Depth Streams

        Top bids and asks, Valid are 5, 10, or 20.

        Stream Names: <symbol>@depth<levels> OR <symbol>@depth<levels>@100ms.
        """
        print(update_time)
        request = self.websocket_request_impl.subscribe_book_depth_event(symbol, limit, update_time, callback, error_handler)
        self.__create_connection(request)

    def subscribe_diff_depth_event(self, symbol: 'str', callback, error_handler=None, update_time: 'UpdateTime'=UpdateTime.INVALID):
        """
        Diff. Depth Stream

        Bids and asks, pushed every 250 milliseconds or 100 milliseconds(if existing)

        Stream Name: <symbol>@depth OR <symbol>@depth@100ms
        """
        request = self.websocket_request_impl.subscribe_diff_depth_event(symbol, update_time, callback, error_handler)
        self.__create_connection(request)

    def subscribe_user_data_event(self, listenKey: 'str', callback, error_handler=None):
        """
        User Data Streams
        """
        request = self.websocket_request_impl.subscribe_user_data_event(listenKey, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_mark_price_event(self, callback, error_handler=None):
        """
        Mark Price Stream for All market

        Mark price and funding rate for all symbols pushed every 3 seconds or every second.

        Stream Name: !markPrice@arr or !markPrice@arr@1s

        Update Speed: 3000ms or 1000ms
        """
        request = self.websocket_request_impl.subscribe_all_mark_price_event(callback, error_handler)
        self.__create_connection(request)

    def subscribe_blvt_info_event(self, symbol, callback, error_handler=None):
        """
        BLVT Info Streams

        Stream Name: <tokenName>@tokenNav

        Note: tokenName must be uppercase, e.g. "TRXDOWN"

        Update Speed: 300ms
        """
        request = self.websocket_request_impl.subscribe_blvt_info_event(symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_blvt_nav_candlestick_event(self, symbol, interval, callback, error_handler=None):
        """
        BLVT NAV Kline/Candlestick Streams

        Stream Name: <tokenName>@nav_Kline_<interval>

        Note: tokenName must be uppercase, e.g. "TRXDOWN"

        Update Speed: 300ms
        """
        request = self.websocket_request_impl.subscribe_blvt_nav_candlestick_event(symbol, interval, callback, error_handler)
        self.__create_connection(request)

    def subscribe_composite_index_event(self, symbol, callback, error_handler=None):
        """
        Composite Index Symbol Information Streams

        Composite index information for index symbols pushed every second.

        Stream Name: <symbol>@compositeIndex

        Update Speed: 1000ms
        """
        request = self.websocket_request_impl.subscribe_composite_index_event(symbol, callback, error_handler)
        self.__create_connection(request)