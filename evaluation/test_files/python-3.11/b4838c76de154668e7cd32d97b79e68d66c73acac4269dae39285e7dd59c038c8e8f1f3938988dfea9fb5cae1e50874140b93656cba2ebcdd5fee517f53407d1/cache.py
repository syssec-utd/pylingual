from qff.tools.logs import log
from qff.price.query import get_price, get_stock_name, get_index_name, get_stock_block
from qff.tools.date import get_trade_min_list
from qff.price.fetch import fetch_current_ticks, fetch_today_min_curve, fetch_price
from qff.frame.context import context
from qff.frame.const import RUN_TYPE
from typing import Optional
import pandas as pd
unit_data_cache = {}

class UnitData:
    """
     当前时刻标的数据快照对象

     通过get_current_data()函数获取，只能在回测或模拟交易中使用

     ================== =====================  =======================================================================
         属性            类型                      说明
     ================== =====================  =======================================================================
     code                str                      标的代码
     name                str                      标的名称
     last_price          float                    当前股票价格
     day_open            float                    当日开盘价
     high_all_day        float                    当日之前时间段最高价
     low_all_day         float                    当日之前时间段最低价
     pre_close           float                    昨日收盘价
     high_limit          float                    当日涨停价
     low_limit           float                    当日跌停价
     last_high           float                    当前Bar最高价
     last_low            float                    当前Bar最低价
     paused              bool                     当日是否停牌
     min_data_before     DataFrame                今日当前时刻之前的分钟曲线
     min_data_freq       str                      当日缓存分钟曲线的频率('1min', '5min', '15min', '30min', '60min')
     high_limit_time     int                      当天涨停时间长度
     block               list                     股票所属板块
     ticks               dict                     当前时刻Tick值，实盘专用
     ================== =====================  =======================================================================

     """

    def __init__(self, code, market='stock'):
        self.code = code
        self.market = market
        self._name = None
        self._block = None
        self._high_limit = None
        self._low_limit = None

    @property
    def high_limit(self):
        """
        [float] 当日涨停价

        """
        if self._high_limit is None:
            self._calc_limit()
        return self._high_limit

    @property
    def low_limit(self):
        """
        [float] 当日跌停价

        """
        if self._low_limit is None:
            self._calc_limit()
        return self._low_limit

    @property
    def name(self):
        """
        [str] 标的名称

        """
        if self._name is None:
            if self.market == 'stock':
                dict_name = get_stock_name(self.code, context.previous_date)
            else:
                dict_name = get_index_name(self.code)
            if dict_name is not None:
                self._name = dict_name[self.code]
            else:
                self._name = 'UNKNOWED'
        return self._name

    @property
    def block(self):
        """
        [list] 股票所属概念板块
        """
        if self._block is None and self.market == 'stock':
            self._block = get_stock_block(self.code)
        return self._block

    def _calc_limit(self):
        if self.code[:3] == '300' and context.previous_date >= '2020-08-24':
            cof = 0.2
        elif self.code[:3] == '688':
            cof = 0.2
        elif 'st' in self.name:
            cof = 0.05
        else:
            cof = 0.1
        self._high_limit = round(self.pre_close * (1 + cof), 2)
        self._low_limit = round(self.pre_close * (1 - cof), 2)

    @property
    def pre_close(self):
        """
        [float] 昨日收盘价
        """
        return 0

    @property
    def day_open(self):
        """
        [float] 今日开盘价
        """
        return 0

    @property
    def paused(self):
        """
        [bool] 是否停盘
        """
        return None

    @property
    def min_data_before(self):
        """
        [DataFrame] 今日当前时刻之前的分钟曲线
        """
        return None

    @property
    def min_data_after(self):
        return None

    @property
    def last_price(self):
        """
        [float] 当前股票价格
        """
        return 0

    @property
    def last_high(self):
        """
        [float] 当前Bar最高价
        """
        return 0

    @property
    def last_low(self):
        """
        [float] 当前Bar最低价
        """
        return 0

    @property
    def high_all_day(self):
        """
        [float] 当日之前时间段最高价
        """
        return 0

    @property
    def low_all_day(self):
        """
        [float] 当日之前时间段最低价
        """
        return 0

    @property
    def min_data_freq(self):
        """
        [str] 当日缓存分钟曲线的频率，回测专用
        """
        return None

    @property
    def high_limit_time(self):
        """
        [int] 当天涨停时间
        """
        return None

    @property
    def ticks(self):
        """
        [Dict] 当前时刻Tick值，实盘专用

        """
        return None

class BacktestData(UnitData):

    def __init__(self, code, market='stock'):
        super().__init__(code, market)
        self._day_buff = get_price(code, end=context.current_dt[0:10], count=2, market=self.market)
        if self._day_buff is None or len(self._day_buff) < 2:
            log.error('获取BacktestData对象失败！code:{},date:{}'.format(code, context.current_dt[0:10]))
            self._pre_close = None
            self._day_open = None
        else:
            self._pre_close = self._day_buff['close'][0]
            self._day_open = self._day_buff['open'][-1]
        self._min_buff = None
        self._min_buff_freq = None

    def _get_min_buff(self):
        for freq in ['1min', '5min', '15min', '30min']:
            data = get_price(self.code, end=context.current_dt[0:10], freq=freq, market=self.market)
            if data is not None:
                self._min_buff = data
                self._min_buff_freq = freq
                break
        if data is None:
            log.error('获取BacktestData对象分钟数据失败！：{}-{}'.format(context.current_dt[0:10], self.code))
            date_list = get_trade_min_list(context.current_dt[0:10])
            data = pd.DataFrame(index=date_list[1:])
            data = data.assign(open=self._day_buff['open'][-1], close=self._day_buff['close'][-1], high=self._day_buff['high'][-1], low=self._day_buff['low'][-1], vol=int(self._day_buff['vol'][-1] / 240), amount=round(self._day_buff['amount'][-1] / 240, 2))
            self._min_buff = data
            self._min_buff_freq = '1min'

    @property
    def pre_close(self):
        return self._pre_close

    @property
    def day_open(self):
        return self._day_open

    @property
    def paused(self):
        return self._day_buff['vol'][-1] < 1

    @property
    def min_data_before(self):
        if self._min_buff is None:
            self._get_min_buff()
        return self._min_buff.loc[:context.current_dt]

    @property
    def min_data_after(self):
        if self._min_buff is None:
            self._get_min_buff()
        return self._min_buff.loc[context.current_dt:]

    @property
    def last_price(self):
        if context.current_dt[11:16] <= '09:30':
            return self._day_open
        else:
            return self.min_data_before.iloc[-1].close

    @property
    def last_high(self):
        if context.current_dt[11:16] <= '09:30':
            return self._day_open
        else:
            return self.min_data_before.iloc[-1].high

    @property
    def last_low(self):
        if context.current_dt[11:16] <= '09:30':
            return self._day_open
        else:
            return self.min_data_before.iloc[-1].low

    @property
    def high_all_day(self):
        if context.current_dt[11:16] <= '09:30':
            return self._day_open
        else:
            return self.min_data_before.high.max()

    @property
    def low_all_day(self):
        if context.current_dt[11:16] <= '09:30':
            return self._day_open
        else:
            return self.min_data_before.low.min()

    @property
    def min_data_freq(self):
        if self._min_buff_freq is None:
            self._get_min_buff()
        return self._min_buff_freq

    @property
    def high_limit_time(self):
        """ 当天涨停时间 """
        if context.current_dt[11:16] <= '09:30':
            return 0
        else:
            freq = int(self.min_data_freq[:-3])
            df = self.min_data_before
            high_limit_count = (pd.Series(df.close >= self.high_limit).sum() + pd.Series(df.open >= self.high_limit).sum() + pd.Series(df.low >= self.high_limit).sum() + pd.Series(df.high >= self.high_limit).sum()) / 4
            return int(high_limit_count * freq)

class RealtimeData(UnitData):

    def __init__(self, code, market='stock'):
        super().__init__(code, market)
        self._ticks = None
        self._bar = None
        self._bar_time = None
        self._name = None

    @property
    def day_open(self):
        if self._ticks is None:
            self._ticks = fetch_current_ticks(self.code, self.market)
        return self._ticks['open']

    @property
    def pre_close(self):
        if self._ticks is None:
            self._ticks = fetch_current_ticks(self.code, self.market)
        return self._ticks['pre_close']

    @property
    def last_price(self):
        if context.run_freq == 'tick' or context.current_dt[11:16] == '09:30':
            self._ticks = fetch_current_ticks(self.code, self.market)
            return self._ticks['price']
        elif self._bar_time == context.current_dt[11:16]:
            return self._bar['close']
        else:
            self._bar = fetch_price(self.code, 1, '1m', self.market)
            self._bar_time = context.current_dt[11:16]
            return self._bar['close']

    @property
    def high_all_day(self):
        self._ticks = fetch_current_ticks(self.code, self.market)
        return self._ticks['high']

    @property
    def low_all_day(self):
        self._ticks = fetch_current_ticks(self.code, self.market)
        return self._ticks['low']

    @property
    def ticks(self):
        self._ticks = fetch_current_ticks(self.code, self.market)
        return self._ticks

    @property
    def min_data_before(self):
        return fetch_today_min_curve(self.code, self.market)

    @property
    def last_high(self):
        if context.run_freq == 'tick' or context.current_dt[11:16] == '09:30':
            self._ticks = fetch_current_ticks(self.code, self.market)
            return self._ticks['price']
        elif self._bar_time == context.current_dt[11:16]:
            return self._bar['high']
        else:
            self._bar = fetch_price(self.code, 1, '1m', self.market)
            self._bar_time = context.current_dt[11:16]
            return self._bar['high']

    @property
    def last_low(self):
        if context.run_freq == 'tick' or context.current_dt[11:16] == '09:30':
            self._ticks = fetch_current_ticks(self.code, self.market)
            return self._ticks['price']
        elif self._bar_time == context.current_dt[11:16]:
            return self._bar['low']
        else:
            self._bar = fetch_price(self.code, 1, '1m', self.market)
            self._bar_time = context.current_dt[11:16]
            return self._bar['low']

    def paused(self):
        self._ticks = fetch_current_ticks(self.code, self.market)
        return self._ticks['vol'] == 0

    @property
    def high_limit_time(self):
        """
        [int] 当天涨停时间
        """
        if context.current_dt[11:16] <= '09:30':
            return 0
        else:
            df = fetch_today_min_curve(self.code, market='stock')
            high_limit_count = (pd.Series(df.close >= self.high_limit).sum() + pd.Series(df.open >= self.high_limit).sum() + pd.Series(df.low >= self.high_limit).sum() + pd.Series(df.high >= self.high_limit).sum()) / 4
            return int(high_limit_count)

def get_current_data(code, market='stock'):
    """
    获取当前时刻标的数据

    获取当前单位时间（当天/当前分钟）的涨跌停价, 是否停牌，当天的开盘价等。
    回测时, 通过其他获取数据的API获取到的是前一个单位时间(天/分钟)的数据, 而有些数据, 我们在这个单位时间是知道的,
    比如涨跌停价, 是否停牌, 当天的开盘价. 我们添加了这个API用来获取这些数据.

    :param code: 股票代码
    :param market: 标的类型，股票还是指数

    :return: 一个 :class:`.UnitData` 对象，代表当前时刻的股票数据


    """
    if market not in ['stock', 'index', 'etf']:
        log.error('get_current_data()出错，market值错误{}'.format(market))
        return None
    security = code + '.' + market
    if security not in unit_data_cache.keys():
        if context.run_type == RUN_TYPE.BACK_TEST:
            unit_data_cache[security] = BacktestData(code, market)
        elif context.run_type == RUN_TYPE.SIM_TRADE:
            unit_data_cache[security] = RealtimeData(code, market)
        else:
            log.error('函数get_current_data()仅支持在回测或模拟交易中使用！')
            return None
    return unit_data_cache[security]

def clear_current_data():
    unit_data_cache.clear()