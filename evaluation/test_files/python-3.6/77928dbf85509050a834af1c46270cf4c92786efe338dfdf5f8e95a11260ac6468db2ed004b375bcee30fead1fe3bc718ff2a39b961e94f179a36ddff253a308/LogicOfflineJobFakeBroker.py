import datetime
import simplejson as json
import random
import string
from enum import Enum
import pandas as pd
from typing import List
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats
from coinlib.broker.BrokerDTO import BrokerSymbol
from coinlib.data.DataTable import DataTable
from coinlib.helper import Serializable, serializeDTO
from coinlib.logics.manager import LogicManager
from coinlib.logics.manager.LogicJobBroker import LogicJobBroker
from coinlib.logics.manager.PortfolioModel import PriceInterface, CurrentMoneyInfo

class OrderType(Enum):
    MARKET = 1
    LIMIT = 2
    STOP_LIMIT = 3

class OrderSide(Enum):
    BUY = 1
    SELL = 2
    LONG = 3
    SHORT = 4

class FakeOrder(Serializable):
    orderId: str
    orderType: OrderType
    side: OrderSide
    order_price: float = None
    executed_price: float = None
    reduceOnly: bool = False
    price: float = None
    symbol: BrokerSymbol
    group: str
    leverage: float = 1
    quantity: float
    stop_price: float
    date: datetime.date

class LogicOfflineJobFakeBroker(LogicJobBroker, PriceInterface):
    _openOrders: [] = []
    _tradesCnt: int
    _portfolioStatistics: [] = []
    _fees: float = 0
    _highestLossPerGroup: float = 0
    _moneyInPortfolio = None
    _lowestPortfolio: float = 999999999
    _portfolioTimeline = []
    _moneyInMarket: CurrentMoneyInfo = None
    _highestProfitPercentage: float = 0
    __highestProfitPerGroup: float = 0
    _moneyInMarketWhenOut: float = None
    _startMoney: float = 0
    _positiveTradePrctg: float = 0
    _negativeTradePrctg: float = 0
    _summaryOfAllPositionpercentages: float = 0
    _positiveAveragePerTrade: float = 0
    _negativeAveragePerTrade: float = 0
    _drawDown: float = 0
    _lowestProfitPercentage: float = 0
    _negativeTradeCnt: float = 0
    _positiveTradeCnt: float = 0
    _currentPortfolioPercentage: float = 0
    _currentPnl: float = 0
    _lastMoney = None
    _portfolioPercentage: float = 0

    def __init__(self, manager: LogicManager):
        super(LogicOfflineJobFakeBroker, self).__init__(manager)
        self._openOrders = []
        self._historicalOrders = []
        self._portfolioStatistics = []
        self._moneyInPortfolio = None
        self.makerFee = manager.getOptions().makerFee
        self.takerFee = manager.getOptions().takerFee
        self._highestProfitPerGroup = 0
        self._currentPortfolioPercentage = 0
        self._moneyInMarket = CurrentMoneyInfo()
        self._startMoney = 0
        self._portfolioTimeline = []
        self._tradesCnt = 0
        self._drawDown = 0
        self._positiveTradeCnt = 0
        self._currentPnl = 0
        self._negativeTradeCnt = 0
        self._startMoney = manager.getPortfolioQuoteMoney()
        self.table = DataTable()
        pass

    def Orders(self) -> List[FakeOrder]:
        return self._historicalOrders

    def time_in(self):
        """
        This method returns the seconds since you are in the market
        """
        if self.imIn():
            if len(self.Orders()) > 0:
                order = self.Orders()[-1]
                now = self.getNow_date()
                distance = (now - order.date).total_seconds()
                return distance
        return -1

    def openOrders(self, type=None) -> List[FakeOrder]:
        if type is not None:
            return list(filter(lambda order: order.orderType == type, self._openOrders))
        return self._openOrders

    def createOrder(self, side: OrderSide, symbol: BrokerSymbol, quantity, type: OrderType=OrderType.MARKET, price=None, leverage=None, clientOrderId: string=None, reduceOnly: bool=False, group=None):
        symbol = self.fillSymbolInfo(symbol)
        if self.getPrice(symbol.symbol) is None:
            return False
        order = FakeOrder()
        letters = string.ascii_lowercase
        result_str = ''.join((random.choice(letters) for i in range(30)))
        order.side = side
        order.reduceOnly = reduceOnly
        order.order_price = self.getPrice(symbol.symbol)
        if clientOrderId is not None:
            order.orderId = clientOrderId
        else:
            order.orderId = result_str
        order.symbol = symbol
        order.executed_price = None
        order.date = self.getNow_date()
        order.date_str = self.getNow()
        order.quantity = quantity
        order.leverage = leverage
        order.group = group
        order.price = price
        order.orderType = type
        if not self.checkIfOrderIsAllowedInCaseOfMoney(order):
            self.onErrorHappenedInBroker('You have not enough Money in your portfolio to do this order', order)
        self.lockQuoteMoney(order)
        self._openOrders.append(order)
        self._historicalOrders.append(order)
        return order

    def checkIfOrderIsAllowedInCaseOfMoney(self, order: FakeOrder):
        if order.side == OrderSide.BUY:
            quoteMoneyAvailable = self.manager.getFreePortfolioQuoteMoney()
            targetMoney = order.quantity * order.order_price
            if targetMoney > quoteMoneyAvailable:
                return False
        return True

    def unlockQuoteMoney(self, order: FakeOrder):
        portfolio = self.manager.getPortfolio()
        portfolio.unlockQuoteMoney(order.symbol.base, order.symbol.quote, order.quantity, order.order_price)
        return False

    def getPortfolioTimeline(self):
        return self.portfolioStatistics

    def lockQuoteMoney(self, order: FakeOrder):
        portfolio = self.manager.getPortfolio()
        portfolio.lockQuoteMoney(order.symbol.base, order.symbol.quote, order.quantity, order.order_price)
        return False

    def getAllAssetsInDataFrame(self):
        charts = []
        d = self.manager.getChartInfo()
        for key in d:
            charts.append({'symbol': d[key]['symbol']['symbol'], 'base': d[key]['symbol']['baseName'], 'quote': d[key]['symbol']['quoteName'], 'timeframe': d[key]['timeframe'], 'chartId': key})
        return charts

    def getChartIdForAsset(self, symbol):
        c = self.getAllAssetsInDataFrame()
        foundCharts = []
        for s in c:
            if s['symbol'] == symbol:
                foundCharts.append(s)
        if len(foundCharts) > 0:
            foundCharts.sort(key=lambda x: x['timeframe'])
            return foundCharts[0]['chartId']
        return None

    def getNow_date(self):
        dt = self.table.getLast('datetime')
        return dt

    def getNow(self):
        dt = self.table.getLast('datetime')
        date = datetime.datetime.strftime(dt, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date

    def getPrice(self, symbol: str=None, base: str=None, quote: str=None):
        if symbol is None:
            price = self.getPrice(symbol=base + '/' + quote)
            if price is not None:
                return price
            price = self.getPrice(symbol=base + '' + quote)
            if price is not None:
                return price
            price = self.getPrice(symbol=base + '-' + quote)
            if price is not None:
                return price
        if isinstance(symbol, BrokerSymbol):
            symbol = symbol.symbol
        chartId = self.getChartIdForAsset(symbol)
        if chartId is None:
            return None
        lastElement = self.table.getLast(chartId + '.main:close')
        if lastElement is None:
            return None
        return lastElement

    def cancelOrder(self, order_id: str):
        selected_order = None
        for order in self._openOrders:
            if order.orderId == order_id:
                selected_order = order
        if selected_order is not None:
            self._openOrders.remove(selected_order)
            return True
        return False

    def buy(self, symbol: BrokerSymbol=None, amount: float=None, amountQuote: float=None, price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        super().buy(symbol, price=price, leverage=leverage, group=group, amount=amount, amountQuote=amountQuote)
        if amount is None:
            amount = self.calculate_amount(amountQuote, symbol)
        if price is None:
            return self.createOrder(OrderSide.BUY, symbol, amount, OrderType.MARKET, price=price, leverage=leverage, group=group)
        else:
            return self.createOrder(OrderSide.BUY, symbol, amount, OrderType.LIMIT, price=price, leverage=leverage, group=group)
        return None

    def sell(self, symbol: BrokerSymbol=None, amount: float=None, amountQuote: float=None, price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        super().sell(symbol, price=price, leverage=leverage, group=group, amount=amount, amountQuote=amountQuote)
        if amount is None:
            amount = self.calculate_amount(amountQuote, symbol)
        if price is None:
            return self.createOrder(OrderSide.SELL, symbol, amount, OrderType.MARKET, price=price, leverage=leverage, group=group)
        else:
            return self.createOrder(OrderSide.SELL, symbol, amount, OrderType.LIMIT, price=price, leverage=leverage, group=group)
        return None

    def buyAll(self, symbol: BrokerSymbol=None, price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        super().buyAll(symbol, price, group=group, leverage=leverage)
        portfolio = self.manager.getPortfolio()
        quoteMoney = portfolio.getQuoteAsset().free * 0.99
        if quoteMoney <= 1:
            raise Exception('Not more than 1 in your portfolio.')
        if price is None:
            current_price = self.getPrice(symbol.symbol)
        else:
            current_price = price
        if current_price is None:
            raise Exception('Price for your symbol can not be found')
        quantity = quoteMoney / current_price
        if price is not None:
            return self.createOrder(OrderSide.BUY, symbol, quantity=quantity, leverage=leverage, type=OrderType.LIMIT, price=price)
        return self.createOrder(OrderSide.BUY, symbol, quantity=quantity, leverage=leverage, type=OrderType.MARKET)

    def sellAll(self, symbol: BrokerSymbol=None, price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        super().sellAll(symbol, price, group=group, leverage=leverage)
        asset = self.manager.getAsset(symbol.base)
        if price is not None:
            return self.createOrder(OrderSide.SELL, symbol, quantity=asset.free, leverage=leverage, type=OrderType.LIMIT, price=price)
        if asset is None:
            raise Exception('We have not found your symbol: ' + symbol.symbol)
        return self.createOrder(OrderSide.SELL, symbol, quantity=asset.free, leverage=leverage, type=OrderType.MARKET)

    def imOut(self):
        return not self.imIn()

    def imIn(self):
        if len(self._openOrders) > 0:
            return True
        if self._moneyInMarket.summary > 1:
            return True
        return False

    def onErrorHappenedInBroker(self, message: str, data):
        raise Exception(message, json.dumps(data, default=serializeDTO))

    def runOrderCalculation(self):
        for order in self._openOrders:
            symbol_price = self.getPrice(order.symbol.symbol)
            if symbol_price is not None:
                if order.orderType == OrderType.MARKET:
                    self.executeOrder(order)
                elif order.orderType == OrderType.LIMIT:
                    if order.side == OrderSide.BUY:
                        if order.price > symbol_price:
                            self.executeOrder(order)
                    elif order.side == OrderSide.SELL:
                        if order.price < symbol_price:
                            self.executeOrder(order)
        return True

    def removeOrderFromOpenOrders(self, order: FakeOrder):
        self._openOrders.remove(order)

    def getStatistics(self):
        stats = statsModel.LogicRunnerStatistics()
        stats.unrealizedProfitPercentage = self._portfolioPercentage
        if self._tradesCnt > 0:
            stats.averageProfitPercentagePergroup = self._summaryOfAllPositionpercentages / self._tradesCnt
        stats.tradesCnt = self._tradesCnt
        stats.winCnt = self._positiveTradeCnt
        stats.lossCnt = self._negativeTradeCnt
        if stats.lossCnt > 0:
            stats.winLossRatio = stats.winCnt / stats.lossCnt
        stats.drawDown = self._lowestProfitPercentage - self._highestProfitPercentage
        stats.highestLossPerGroup = self._highestLossPerGroup
        stats.highestLossPercentage = self._lowestProfitPercentage
        stats.highestProfitPerGroup = self._highestProfitPerGroup
        stats.highestProfitPercentage = self._highestProfitPercentage
        stats.fees = self._fees
        money = statsModel.CalculatedBaseMoney()
        stats.calculatedMoney.CopyFrom(money)
        stats.portfolioTimeline = json.dumps(self._portfolioTimeline)
        return stats

    def calculateStatistics(self):
        self._moneyInPortfolio = self.manager.getPortfolioQuoteMoney()
        self._portfolioPercentage = (self._moneyInPortfolio / self._startMoney - 1) * 100
        if self._lastMoney is not None and self._lastMoney != self._moneyInPortfolio:
            self._portfolioTimeline.append({'date': self.getNow(), 'portfolioMoney': self._moneyInPortfolio})
        self._lastMoney = self._moneyInPortfolio
        return True

    def executeOrder(self, order: FakeOrder):
        self._tradesCnt = self._tradesCnt + 1
        symbol_price = self.getPrice(order.symbol.symbol)
        if symbol_price is None:
            print('ERROR')
        order.executed_price = symbol_price
        if order.side == OrderSide.BUY:
            self.manager.saveInfo('trader', 'buyExecuted', {'clientOrderId': order.orderId, 'group': order.group})
        elif order.side == OrderSide.SELL:
            self.manager.saveInfo('trader', 'sellExecuted', {'clientOrderId': order.orderId, 'group': order.group})
        elif order.side == OrderSide.SHORT:
            self.manager.saveInfo('trader', 'shortExecuted', {'clientOrderId': order.orderId, 'group': order.group})
        elif order.side == OrderSide.LONG:
            self.manager.saveInfo('trader', 'longExecuted', {'clientOrderId': order.orderId, 'group': order.group})
        self.removeOrderFromOpenOrders(order)
        self.unlockQuoteMoney(order)
        self.onHandleExecutedOrder(order)
        self.onAfterOrderExecutionFinished(order)

    def recalculateCurrentPortfolioByAssets(self, updatePortfolio=True):
        portfolio = self.manager.getPortfolio()
        summary = 0
        free = 0
        locked = 0
        quoteCurrency = portfolio.currentMoney.name
        for asset in portfolio.assets:
            if asset.name == quoteCurrency:
                summary = summary + asset.total
                free = free + asset.free
                locked = locked + asset.locked
            else:
                try:
                    price = self.getPrice(base=asset.name, quote=quoteCurrency)
                    if price is not None:
                        summary = summary + asset.total * price
                        free = free + asset.free * price
                        locked = locked + asset.locked * price
                except Exception as e:
                    pass
        portfolio.currentMoney.free = free
        portfolio.currentMoney.summary = summary
        portfolio.currentMoney.locked = locked
        portfolio.currentMoney.date = self.getNow()
        if updatePortfolio:
            self.manager.updatePortfolio(portfolio)
        return portfolio

    def getCurrentMoneyInMarket(self):
        portfolio = self.manager.getPortfolio()
        summary = 0
        free = 0
        locked = 0
        quoteCurrency = portfolio.currentMoney.name
        for asset in portfolio.assets:
            if asset.name != quoteCurrency:
                try:
                    price = self.getPrice(base=asset.name, quote=quoteCurrency)
                    if price is not None:
                        summary = asset.total * price
                        free = asset.free * price
                        locked = asset.locked * price
                except Exception as e:
                    pass
        moneyInMarket = CurrentMoneyInfo()
        moneyInMarket.free = free
        moneyInMarket.summary = summary
        return moneyInMarket

    def onAfterOrderExecutionFinished(self, order):
        self.recalculateCurrentPortfolioByAssets()
        wasIn = False
        if self._moneyInMarket.summary > 1:
            wasIn = True
        self._moneyInMarket = self.getCurrentMoneyInMarket()
        if self._moneyInMarket.summary > 1 and wasIn is False:
            self._moneyInMarketWhenOut = self._moneyInPortfolio
        if self._moneyInMarket.summary > 1:
            if order is not None:
                current_price = self.getPrice(order.symbol)
                if order.side == OrderSide.BUY:
                    self._currentPnl = (current_price / order.executed_price - 1) * 100
                else:
                    self._currentPnl = (order.executed_price / current_price - 1) * 100
        if wasIn and self._moneyInMarket.summary < 1:
            difference = self._moneyInPortfolio - self._moneyInMarketWhenOut
            differencePercentage = (1 - self._moneyInMarketWhenOut / self._moneyInPortfolio) * 100
            self._summaryOfAllPositionpercentages = self._summaryOfAllPositionpercentages + abs(differencePercentage)
            if differencePercentage < self._highestLossPerGroup:
                self._highestLossPerGroup = differencePercentage
            if differencePercentage > self._highestProfitPerGroup:
                self._highestProfitPerGroup = differencePercentage
            if difference > 0:
                self._positiveTradeCnt = self._positiveTradeCnt + 1
                self._positiveTradePrctg = self._positiveTradePrctg + differencePercentage
                self._positiveAveragePerTrade = self._positiveTradePrctg / self._positiveTradeCnt
            else:
                self._negativeTradeCnt = self._negativeTradeCnt + 1
                self._negativeTradePrctg = self._negativeTradePrctg + differencePercentage
                self._negativeAveragePerTrade = self._negativeTradePrctg / self._negativeTradeCnt
        self._currentPortfolioPercentage = (self._moneyInPortfolio / self._startMoney - 1) * 100
        if self._currentPortfolioPercentage > self._highestProfitPercentage:
            self._highestProfitPercentage = self._currentPortfolioPercentage
        if self._currentPortfolioPercentage < self._lowestProfitPercentage:
            self._lowestProfitPercentage = self._currentPortfolioPercentage
        return True

    def getTable(self):
        return self.df

    def setTable(self, table):
        self.table = table

    def currentMarkPrice(self):
        return None

    def profitFuture(self):
        return self._currentPnl

    def profitGroup(self, group):
        return self._currentPnl

    def lastOrders(self):
        return self.Orders()

    def currentOrder(self):
        return self.Orders()[-1]

    def currentPNL(self):
        return self._currentPnl