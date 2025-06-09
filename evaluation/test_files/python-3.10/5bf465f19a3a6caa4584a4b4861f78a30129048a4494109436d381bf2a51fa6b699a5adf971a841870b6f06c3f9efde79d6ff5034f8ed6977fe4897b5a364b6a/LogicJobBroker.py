import math
from typing import List
from coinlib.broker.BrokerDTO import BrokerDetailedInfo, BrokerSymbol, Position
from coinlib.logics.manager import LogicManager

class WrongArgumentError(Exception):
    pass

class LogicJobBroker:
    manager: LogicManager = None

    def __init__(self, manager: LogicManager):
        self.manager = manager
        pass

    def fillSymbolInfo(self, symbol: BrokerSymbol):
        if symbol.symbol is not None:
            symbol = BrokerSymbol(symbol.symbol)
        return symbol

    def getManager(self) -> LogicManager:
        return self.manager

    def profitFuture(self):
        return None

    def profitGroup(self, group):
        return None

    def time_in(self):
        return False

    def getLoop(self):
        return None

    def runAsync(self, method):
        return self.getLoop().run_until_complete(method)

    def traderName(self):
        return self.manager.getName()

    def isFuture(self):
        return self.manager.isFuture()

    def isSpot(self):
        return self.manager.isSpot()

    def isMargin(self):
        return self.manager.isMargin()

    def isOption(self):
        return self.manager.isOption()

    def canLeverage(self):
        return False

    def brokerDetails(self) -> BrokerDetailedInfo:
        return None

    def imIn(self):
        return False

    def price(self, base, quote):
        return None

    def imOut(self):
        return True

    def openOrders(self, type=None):
        return []

    def positions(self) -> [Position]:
        return []

    def closePosition(self, clientOrderId, price: float=None, amount=None, symbol=None, group=None):
        self.manager.saveInfo('trader', 'closePosition', {'clientOrderId': clientOrderId, 'amount': amount, 'symbol': symbol.symbol if symbol is not None else '', 'price': price, 'group': group})
        return False

    def buyAll(self, symbol: BrokerSymbol, price: float=None, leverage: float=None, group=None):
        self.manager.saveInfo('trader', 'buyAll', {'amount': 100, 'symbol': symbol.symbol, 'leverage': leverage, 'price': price, 'group': group})
        return False

    def sellAll(self, symbol: BrokerSymbol, price: float=None, leverage: float=None, group=None):
        self.manager.saveInfo('trader', 'sellAll', {'amount': 100, 'symbol': symbol.symbol, 'leverage': leverage, 'price': price, 'group': group})
        return False

    def getAssets(self):
        return self.manager.getAssets()

    def error(self):
        return False

    def truncate(self, a, n):
        return math.floor(a * 10 ** n) / 10 ** n

    def calculate_amount(self, amount_in_quote_money: float, symbol: BrokerSymbol):
        price = self.price(symbol['base'], symbol['quote'])
        volume = amount_in_quote_money / price
        volume = self.truncate(volume, symbol['size_precision'])
        return volume

    async def symbols_async(self):
        return []

    def symbols(self) -> List[BrokerSymbol]:
        return []

    def buy(self, symbol: BrokerSymbol=None, amount=None, amountQuote=None, price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        self.manager.saveInfo('trader', 'buy', {'symbol': symbol.symbol, 'amount': amount, 'amountQuote': amountQuote, 'price': price, 'group': group})
        return False

    def sell(self, symbol: BrokerSymbol=None, amount=None, amountQuote=None, price=None, leverage=None, group=None):
        if symbol is None:
            symbol = self.manager.getSymbolForChart()
        symbol = self.fillSymbolInfo(symbol)
        self.manager.saveInfo('trader', 'sell', {'symbol': symbol.symbol, 'amountQuote': amountQuote, 'amount': amount, 'price': price, 'group': group})
        return False

    def printDebug(self):
        return None

    def longAll(self, symbol: BrokerSymbol=None, price=None, leverage=None, group=None, maximum=None, maximumQuote=None):
        if symbol is None or isinstance(symbol, str) or symbol.symbol is None:
            raise WrongArgumentError('Please use a symbol object to use any brokerage  method')
        self.manager.saveInfo('trader', 'longAll', {'symbol': symbol.symbol, 'price': price, 'group': group})
        return True

    def shortAll(self, symbol: BrokerSymbol=None, price=None, leverage=None, group=None, maximum=None, maximumQuote=None):
        if symbol is None or isinstance(symbol, str) or symbol.symbol is None:
            raise WrongArgumentError('Please use a symbol object to use any brokerage  method')
        self.manager.saveInfo('trader', 'shortAll', {'symbol': symbol.symbol, 'price': price, 'group': group})
        return True

    def long(self, symbol: BrokerSymbol=None, amount: float=None, amountQuote=None, price=None, leverage=None, group=None):
        if symbol is None or isinstance(symbol, str) or symbol.symbol is None:
            raise WrongArgumentError('Please use a symbol object to use any brokerage  method')
        self.manager.saveInfo('trader', 'long', {'symbol': symbol.symbol, 'amount': amount, 'amountQuote': amountQuote, 'price': price, 'group': group})
        return True

    def short(self, symbol: BrokerSymbol=None, amount: float=None, amountQuote=None, price=None, leverage=None, group=None):
        if symbol is None or isinstance(symbol, str) or symbol.symbol is None:
            raise WrongArgumentError('Please use a symbol object to use any brokerage  method')
        self.manager.saveInfo('trader', 'short', {'symbol': symbol.symbol, 'amount': amount, 'amountQuote': amountQuote, 'price': price, 'group': group})
        return True

    def getOrderTypes(self):
        return []

    def getPossibleLeverage(self):
        return False

    def getTradingRules(self):
        return None

    def closeAllPositions(self, group=None):
        self.manager.saveInfo('trader', 'closeAllPositions', {'group': group})
        return False

    def currentMargin(self):
        return False

    def cancelOrder(self, order_id: str):
        self.manager.saveInfo('trader', 'cancelOrder', {'order_id': order_id})
        return False

    def lastOrders(self):
        return False

    def currentOrder(self):
        return None

    def sessionPNL(self):
        return None

    def currentPNL(self):
        return None

    def currentMarkPrice(self):
        return None