from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C', '#44488E', '#BA67E9', '#3FAEEE', '#DC494F', '#9EA2C9']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C', '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7', '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']

def from_rgb_to_color16(rgb):
    color = '#'
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color

def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return (calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df)

class Performance:

    def __init__(self, comparison, start_date, end_date, data_path, mutual_fund_list, private_fund_list):
        self.comparison = comparison
        self.start_date = start_date
        self.end_date = end_date
        self.data_path = data_path + comparison + '/'
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        self.mutual_fund_list = mutual_fund_list
        self.private_fund_list = private_fund_list
        self.fund_name_dic = pd.read_excel(data_path + 'fund.xlsx')[['基金代码', '基金名称']].dropna().set_index('基金代码')['基金名称'].to_dict()
        self.rank_list = [self.fund_name_dic[i] for i in mutual_fund_list + private_fund_list]
        self.load()

    def load(self):
        (self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df) = get_date(self.start_date, self.end_date)
        (mutual_fund_nav_list, private_fund_nav_list) = ([], [])
        (mutual_fund_achievement_list, private_fund_achievement_list) = ([], [])
        (mutual_fund_return_period_list, private_fund_return_period_list) = ([], [])
        (mutual_fund_return_year_list, private_fund_return_year_list) = ([], [])
        (mutual_fund_return_month_list, private_fund_return_month_list) = ([], [])
        if len(mutual_fund_list) != 0:
            for fund_id in mutual_fund_list:
                fund_nav = HBDB().read_fund_cumret_given_code(fund_id, self.start_date, self.end_date)
                if len(fund_nav) == 0:
                    fund_nav = pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'CUM_RET'])
                fund_nav['TRADE_DATE'] = fund_nav['TRADE_DATE'].astype(str)
                fund_nav = fund_nav.sort_values('TRADE_DATE')
                fund_nav['ADJ_NAV'] = 0.01 * fund_nav['CUM_RET'] + 1
                fund_nav = fund_nav[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']]
                mutual_fund_nav_list.append(fund_nav)
                fund_achievement = pd.DataFrame(index=[fund_id], columns=['年化收益率', '年化波动率', '最大回撤', '年化夏普比率', '卡玛比率', '投资胜率'])
                fund_return = HBDB().read_fund_return_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'))
                fund_return = fund_return if len(fund_return) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'rqnp', 'jzrq', 'zbnp', 'zbnhnp'])
                fund_return = fund_return.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'rqnp': 'START_DATE', 'jzrq': 'END_DATE', 'zbnp': 'RETURN', 'zbnhnp': 'ANNUAL_RETURN'})
                fund_return['END_DATE'] = fund_return['END_DATE'].astype(str)
                fund_return = fund_return[fund_return['END_DATE'] == max(fund_return['END_DATE'])]
                fund_return['TYPE'] = fund_return['TYPE'].astype(int)
                fund_return = fund_return[fund_return['TYPE'] == 2999]
                fund_volatility = HBDB().read_fund_volatility_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'))
                fund_volatility = fund_volatility if len(fund_volatility) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'tjrq', 'zbnp', 'nhzbnp'])
                fund_volatility = fund_volatility.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'tjrq': 'END_DATE', 'zbnp': 'VOLATILITY', 'nhzbnp': 'ANNUAL_VOLATILITY'})
                fund_volatility['END_DATE'] = fund_volatility['END_DATE'].astype(str)
                fund_volatility = fund_volatility[fund_volatility['END_DATE'] == max(fund_volatility['END_DATE'])]
                fund_volatility['TYPE'] = fund_volatility['TYPE'].astype(int)
                fund_volatility = fund_volatility[fund_volatility['TYPE'] == 2999]
                fund_maxdrawdown = HBDB().read_fund_maxdrawdown_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'))
                fund_maxdrawdown = fund_maxdrawdown if len(fund_maxdrawdown) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp'])
                fund_maxdrawdown = fund_maxdrawdown.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'MAX_DRAWDOWN'})
                fund_maxdrawdown['END_DATE'] = fund_maxdrawdown['END_DATE'].astype(str)
                fund_maxdrawdown = fund_maxdrawdown[fund_maxdrawdown['END_DATE'] == max(fund_maxdrawdown['END_DATE'])]
                fund_maxdrawdown['TYPE'] = fund_maxdrawdown['TYPE'].astype(int)
                fund_maxdrawdown = fund_maxdrawdown[fund_maxdrawdown['TYPE'] == 2999]
                fund_sharpe = HBDB().read_fund_sharpe_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'))
                fund_sharpe = fund_sharpe if len(fund_sharpe) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'tjrq', 'zbnp', 'nhzbnp'])
                fund_sharpe = fund_sharpe.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'tjrq': 'END_DATE', 'zbnp': 'SHARPE_RATIO', 'nhzbnp': 'ANNUAL_SHARPE_RATIO'})
                fund_sharpe['END_DATE'] = fund_sharpe['END_DATE'].astype(str)
                fund_sharpe = fund_sharpe[fund_sharpe['END_DATE'] == max(fund_sharpe['END_DATE'])]
                fund_sharpe['TYPE'] = fund_sharpe['TYPE'].astype(int)
                fund_sharpe = fund_sharpe[fund_sharpe['TYPE'] == 2999]
                fund_calmar = HBDB().read_fund_calmar_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'))
                fund_calmar = fund_calmar if len(fund_calmar) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp'])
                fund_calmar = fund_calmar.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'CALMAR_RATIO'})
                fund_calmar['END_DATE'] = fund_calmar['END_DATE'].astype(str)
                fund_calmar = fund_calmar[fund_calmar['END_DATE'] == max(fund_calmar['END_DATE'])]
                fund_calmar['TYPE'] = fund_calmar['TYPE'].astype(int)
                fund_calmar = fund_calmar[fund_calmar['TYPE'] == 2999]
                fund_winratio = HBDB().read_fund_winratio_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m'))
                fund_winratio = fund_winratio if len(fund_winratio) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'tjyf', 'zbnp'])
                fund_winratio = fund_winratio.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'tjyf': 'END_DATE', 'zbnp': 'WIN_RATIO'})
                fund_winratio['END_DATE'] = fund_winratio['END_DATE'].astype(str)
                fund_winratio = fund_winratio[fund_winratio['END_DATE'] == max(fund_winratio['END_DATE'])]
                fund_winratio['TYPE'] = fund_winratio['TYPE'].astype(int)
                fund_winratio = fund_winratio[fund_winratio['TYPE'] == 2999]
                fund_achievement.loc[fund_id, '年化收益率'] = fund_return['ANNUAL_RETURN'].values[0] if len(fund_return) > 0 else np.nan
                fund_achievement.loc[fund_id, '年化波动率'] = fund_volatility['ANNUAL_VOLATILITY'].values[0] if len(fund_volatility) > 0 else np.nan
                fund_achievement.loc[fund_id, '最大回撤'] = fund_maxdrawdown['MAX_DRAWDOWN'].values[0] if len(fund_maxdrawdown) > 0 else np.nan
                fund_achievement.loc[fund_id, '年化夏普比率'] = fund_sharpe['ANNUAL_SHARPE_RATIO'].values[0] if len(fund_sharpe) > 0 else np.nan
                fund_achievement.loc[fund_id, '卡玛比率'] = fund_calmar['CALMAR_RATIO'].values[0] if len(fund_calmar) > 0 else np.nan
                fund_achievement.loc[fund_id, '投资胜率'] = fund_winratio['WIN_RATIO'].values[0] if len(fund_winratio) > 0 else np.nan
                mutual_fund_achievement_list.append(fund_achievement)
                fund_return_period = HBDB().read_fund_return_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(30)).strftime('%Y%m%d'))
                fund_return_period = fund_return_period.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'RETURN_TYPE', 'rqnp': 'START_DATE', 'jzrq': 'END_DATE', 'zbnp': 'RETURN', 'zbnhnp': 'ANNUAL_RETURN'})
                fund_return_period['END_DATE'] = fund_return_period['END_DATE'].astype(str)
                fund_return_period = fund_return_period[fund_return_period['END_DATE'] == max(fund_return_period['END_DATE'])]
                fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].astype(int)
                fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].replace({2998: '今年以来', 2101: '近1月', 2103: '近3月', 2106: '近6月', 2201: '近1年', 2202: '近2年', 2203: '近3年'})
                fund_return_period = fund_return_period[fund_return_period['RETURN_TYPE'].isin(['今年以来', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年'])]
                fund_return_period = fund_return_period.pivot(index='FUND_CODE', columns='RETURN_TYPE', values='RETURN')
                fund_return_period = fund_return_period[['今年以来', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年']]
                mutual_fund_return_period_list.append(fund_return_period)
                fund_return_year = HBDB().read_fund_return_year_given_code(fund_id)
                fund_return_year = fund_return_year.rename(columns={'jjdm': 'FUND_CODE', 'tjnf': 'YEAR', 'hb1n': 'RETURN_YEAR'})
                fund_return_year['YEAR'] = fund_return_year['YEAR'].astype(str)
                fund_return_year = fund_return_year[['FUND_CODE', 'YEAR', 'RETURN_YEAR']]
                mutual_fund_return_year_list.append(fund_return_year)
                fund_return_month = HBDB().read_fund_return_month_given_code(fund_id)
                fund_return_month = fund_return_month.rename(columns={'jjdm': 'FUND_CODE', 'tjyf': 'MONTH', 'hb1y': 'RETURN_MONTH'})
                fund_return_month['MONTH'] = fund_return_month['MONTH'].astype(str)
                fund_return_month = fund_return_month[['FUND_CODE', 'MONTH', 'RETURN_MONTH']]
                mutual_fund_return_month_list.append(fund_return_month)
        if len(private_fund_list) != 0:
            for fund_id in private_fund_list:
                fund_nav = HBDB().read_private_fund_cumret_given_code(fund_id, self.start_date, self.end_date)
                if len(fund_nav) == 0:
                    fund_nav = pd.DataFrame(columns=['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV'])
                fund_nav['TRADE_DATE'] = fund_nav['TRADE_DATE'].astype(str)
                fund_nav = fund_nav.sort_values('TRADE_DATE')
                fund_nav = fund_nav[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV']]
                private_fund_nav_list.append(fund_nav)
                fund_achievement = pd.DataFrame(index=[fund_id], columns=['年化收益率', '年化波动率', '最大回撤', '年化夏普比率', '卡玛比率', '投资胜率'])
                fund_return = HBDB().read_private_fund_return_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_return = fund_return if len(fund_return) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'rqnp', 'jzrq', 'zbnp', 'zbnhnp'])
                fund_return = fund_return.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'rqnp': 'START_DATE', 'jzrq': 'END_DATE', 'zbnp': 'RETURN', 'nhzbnp': 'ANNUAL_RETURN'})
                fund_return['END_DATE'] = fund_return['END_DATE'].astype(str)
                fund_return = fund_return[fund_return['END_DATE'] == max(fund_return['END_DATE'])]
                fund_return['TYPE'] = fund_return['TYPE'].astype(int)
                fund_return = fund_return[fund_return['TYPE'] == 2999]
                fund_volatility = HBDB().read_private_fund_volatility_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_volatility = fund_volatility if len(fund_volatility) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp', 'nhzbnp'])
                fund_volatility = fund_volatility.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'VOLATILITY', 'nhzbnp': 'ANNUAL_VOLATILITY'})
                fund_volatility['END_DATE'] = fund_volatility['END_DATE'].astype(str)
                fund_volatility = fund_volatility[fund_volatility['END_DATE'] == max(fund_volatility['END_DATE'])]
                fund_volatility['TYPE'] = fund_volatility['TYPE'].astype(int)
                fund_volatility = fund_volatility[fund_volatility['TYPE'] == 2999]
                fund_maxdrawdown = HBDB().read_private_fund_maxdrawdown_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_maxdrawdown = fund_maxdrawdown if len(fund_maxdrawdown) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp'])
                fund_maxdrawdown = fund_maxdrawdown.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'MAX_DRAWDOWN'})
                fund_maxdrawdown['END_DATE'] = fund_maxdrawdown['END_DATE'].astype(str)
                fund_maxdrawdown = fund_maxdrawdown[fund_maxdrawdown['END_DATE'] == max(fund_maxdrawdown['END_DATE'])]
                fund_maxdrawdown['TYPE'] = fund_maxdrawdown['TYPE'].astype(int)
                fund_maxdrawdown = fund_maxdrawdown[fund_maxdrawdown['TYPE'] == 2999]
                fund_sharpe = HBDB().read_private_fund_sharpe_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_sharpe = fund_sharpe if len(fund_sharpe) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp', 'nhzbnp'])
                fund_sharpe = fund_sharpe.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'SHARPE_RATIO', 'nhzbnp': 'ANNUAL_SHARPE_RATIO'})
                fund_sharpe['END_DATE'] = fund_sharpe['END_DATE'].astype(str)
                fund_sharpe = fund_sharpe[fund_sharpe['END_DATE'] == max(fund_sharpe['END_DATE'])]
                fund_sharpe['TYPE'] = fund_sharpe['TYPE'].astype(int)
                fund_sharpe = fund_sharpe[fund_sharpe['TYPE'] == 2999]
                fund_calmar = HBDB().read_private_fund_calmar_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_calmar = fund_calmar if len(fund_calmar) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp'])
                fund_calmar = fund_calmar.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'CALMAR_RATIO'})
                fund_calmar['END_DATE'] = fund_calmar['END_DATE'].astype(str)
                fund_calmar = fund_calmar[fund_calmar['END_DATE'] == max(fund_calmar['END_DATE'])]
                fund_calmar['TYPE'] = fund_calmar['TYPE'].astype(int)
                fund_calmar = fund_calmar[fund_calmar['TYPE'] == 2999]
                fund_winratio = HBDB().read_private_fund_winratio_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_winratio = fund_winratio if len(fund_winratio) > 0 else pd.DataFrame(index=[0], columns=['jjdm', 'zblb', 'jzrq', 'zbnp'])
                fund_winratio = fund_winratio.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'TYPE', 'jzrq': 'END_DATE', 'zbnp': 'WIN_RATIO'})
                fund_winratio['END_DATE'] = fund_winratio['END_DATE'].astype(str)
                fund_winratio = fund_winratio[fund_winratio['END_DATE'] == max(fund_winratio['END_DATE'])]
                fund_winratio['TYPE'] = fund_winratio['TYPE'].astype(int)
                fund_winratio = fund_winratio[fund_winratio['TYPE'] == 2999]
                fund_achievement.loc[fund_id, '年化收益率'] = fund_return['ANNUAL_RETURN'].values[0] if len(fund_return) > 0 else np.nan
                fund_achievement.loc[fund_id, '年化波动率'] = fund_volatility['ANNUAL_VOLATILITY'].values[0] if len(fund_volatility) > 0 else np.nan
                fund_achievement.loc[fund_id, '最大回撤'] = fund_maxdrawdown['MAX_DRAWDOWN'].values[0] if len(fund_maxdrawdown) > 0 else np.nan
                fund_achievement.loc[fund_id, '年化夏普比率'] = fund_sharpe['ANNUAL_SHARPE_RATIO'].values[0] if len(fund_sharpe) > 0 else np.nan
                fund_achievement.loc[fund_id, '卡玛比率'] = fund_calmar['CALMAR_RATIO'].values[0] if len(fund_calmar) > 0 else np.nan
                fund_achievement.loc[fund_id, '投资胜率'] = fund_winratio['WIN_RATIO'].values[0] if len(fund_winratio) > 0 else np.nan
                private_fund_achievement_list.append(fund_achievement)
                fund_return_period = HBDB().read_private_fund_return_period_given_code_and_date(fund_id, (datetime.strptime(self.end_date, '%Y%m%d') - timedelta(365)).strftime('%Y%m%d'))
                fund_return_period = fund_return_period.rename(columns={'jjdm': 'FUND_CODE', 'zblb': 'RETURN_TYPE', 'rqnp': 'START_DATE', 'jzrq': 'END_DATE', 'zbnp': 'RETURN', 'nhzbnp': 'ANNUAL_RETURN'})
                fund_return_period['END_DATE'] = fund_return_period['END_DATE'].astype(str)
                fund_return_period = fund_return_period[fund_return_period['END_DATE'] == max(fund_return_period['END_DATE'])]
                fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].astype(int)
                fund_return_period['RETURN_TYPE'] = fund_return_period['RETURN_TYPE'].replace({2998: '今年以来', 2101: '近1月', 2103: '近3月', 2106: '近6月', 2201: '近1年', 2202: '近2年', 2203: '近3年'})
                fund_return_period = fund_return_period[fund_return_period['RETURN_TYPE'].isin(['今年以来', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年'])]
                fund_return_period = fund_return_period.pivot(index='FUND_CODE', columns='RETURN_TYPE', values='RETURN')
                fund_return_period = fund_return_period[['今年以来', '近1月', '近3月', '近6月', '近1年', '近2年', '近3年']]
                private_fund_return_period_list.append(fund_return_period)
                fund_return_year = HBDB().read_private_fund_return_year_given_code(fund_id)
                fund_return_year = fund_return_year.rename(columns={'jjdm': 'FUND_CODE', 'hblb': 'RETURN_TYPE', 'tjnf': 'YEAR', 'hb1n': 'RETURN_YEAR', 'nhhb1n': 'ANNUAL_RETURN_YEAR'})
                fund_return_year['YEAR'] = fund_return_year['YEAR'].astype(str)
                fund_return_year['RETURN_TYPE'] = fund_return_year['RETURN_TYPE'].astype(int)
                fund_return_year = fund_return_year[fund_return_year['RETURN_TYPE'] == 1]
                fund_return_year = fund_return_year[['FUND_CODE', 'YEAR', 'RETURN_YEAR']]
                private_fund_return_year_list.append(fund_return_year)
                fund_return_month = HBDB().read_private_fund_return_month_given_code(fund_id)
                fund_return_month = fund_return_month.rename(columns={'jjdm': 'FUND_CODE', 'tjyf': 'MONTH', 'hb1y': 'RETURN_MONTH'})
                fund_return_month['MONTH'] = fund_return_month['MONTH'].astype(str)
                fund_return_month = fund_return_month[['FUND_CODE', 'MONTH', 'RETURN_MONTH']]
                private_fund_return_month_list.append(fund_return_month)
        self.fund_nav = pd.concat(mutual_fund_nav_list + private_fund_nav_list)
        self.fund_nav = self.fund_nav.pivot(index='TRADE_DATE', columns='FUND_CODE', values='ADJ_NAV').sort_index()
        self.fund_nav = self.fund_nav.reindex(self.calendar_df[self.calendar_df['IS_OPEN'] == 1]['CALENDAR_DATE'].unique().tolist()).interpolate().dropna().sort_index()
        self.fund_nav = self.fund_nav[self.fund_nav.index.isin(self.calendar_df[self.calendar_df['IS_WEEK_END'] == '1']['CALENDAR_DATE'].unique().tolist())].sort_index()
        self.fund_nav = self.fund_nav / self.fund_nav.iloc[0]
        self.fund_achievement = pd.concat(mutual_fund_achievement_list + private_fund_achievement_list)
        self.fund_achievement = self.fund_achievement.replace(99999.0, np.nan)
        self.fund_achievement[['年化收益率', '年化波动率', '最大回撤', '投资胜率']] = 0.01 * self.fund_achievement[['年化收益率', '年化波动率', '最大回撤', '投资胜率']]
        self.fund_achievement.index = [self.fund_name_dic[i] for i in list(self.fund_achievement.index)]
        self.fund_return_period = pd.concat(mutual_fund_return_period_list + private_fund_return_period_list)
        self.fund_return_period = self.fund_return_period.replace(99999.0, np.nan)
        self.fund_return_period = 0.01 * self.fund_return_period
        self.fund_return_period.index = [self.fund_name_dic[i] for i in list(self.fund_return_period.index)]
        self.fund_return_year = pd.concat(mutual_fund_return_year_list + private_fund_return_year_list)
        self.fund_return_year = self.fund_return_year.pivot(index='FUND_CODE', columns='YEAR', values='RETURN_YEAR').sort_index()
        self.fund_return_year = self.fund_return_year.replace(99999.0, np.nan)
        self.fund_return_year = 0.01 * self.fund_return_year
        self.fund_return_year.index = [self.fund_name_dic[i] for i in list(self.fund_return_year.index)]
        self.fund_return_year = self.fund_return_year.reset_index()
        self.fund_return_year['index'] = self.fund_return_year['index'].astype('category')
        self.fund_return_year['index'].cat.reorder_categories(self.rank_list, inplace=True)
        self.fund_return_year = self.fund_return_year.sort_values('index').set_index('index')
        self.fund_return_month = pd.concat(mutual_fund_return_month_list + private_fund_return_month_list)
        self.fund_return_month['YEAR'] = self.fund_return_month['MONTH'].apply(lambda x: int(str(x)[:4]))
        self.fund_return_month['MONTH'] = self.fund_return_month['MONTH'].apply(lambda x: int(str(x)[4:]))
        self.fund_return_month['FUND_NAME'] = self.fund_return_month['FUND_CODE'].apply(lambda x: self.fund_name_dic[x])
        self.fund_return_month = self.fund_return_month.pivot(index=['YEAR', 'FUND_NAME'], columns='MONTH', values='RETURN_MONTH').sort_index()
        self.fund_return_month = self.fund_return_month.replace(99999.0, np.nan)
        self.fund_return_month = 0.01 * self.fund_return_month
        self.fund_return_month.columns = map(lambda x: '{0}月'.format(x), self.fund_return_month.columns)
        self.fund_return_month = self.fund_return_month.reset_index()
        self.fund_return_month['FUND_NAME'] = self.fund_return_month['FUND_NAME'].astype('category')
        self.fund_return_month['FUND_NAME'].cat.reorder_categories(self.rank_list, inplace=True)
        self.fund_return_month = self.fund_return_month.sort_values(['YEAR', 'FUND_NAME']).set_index(['YEAR', 'FUND_NAME'])
        return

    def get_result(self):
        fund_nav = self.fund_nav.copy(deep=True)
        print(fund_nav.index.min(), fund_nav.index.max())
        fund_nav.index = map(lambda x: datetime.strptime(x, '%Y%m%d'), fund_nav.index)
        plt.figure(figsize=(12, 6))
        if self.comparison == '朱雀':
            for (i, fund_id) in enumerate(mutual_fund_list):
                plt.plot(fund_nav.index, fund_nav[fund_id], label=self.fund_name_dic[fund_id], linestyle='-', linewidth=2.5, color=line_color_list[0])
            for (i, fund_id) in enumerate(private_fund_list):
                plt.plot(fund_nav.index, fund_nav[fund_id], label=self.fund_name_dic[fund_id], linestyle='-', linewidth=2.5, color=line_color_list[1])
        elif self.comparison == '中观轮动':
            for (i, fund_id) in enumerate(mutual_fund_list):
                plt.plot(fund_nav.index, fund_nav[fund_id], label=self.fund_name_dic[fund_id], linestyle='-', linewidth=2, color=line_color_list[i])
            for (i, fund_id) in enumerate(private_fund_list):
                plt.plot(fund_nav.index, fund_nav[fund_id], label=self.fund_name_dic[fund_id], linestyle='--', linewidth=2, color=line_color_list[i])
        else:
            for (i, fund_id) in enumerate(mutual_fund_list):
                plt.plot(fund_nav.index, fund_nav[fund_id], label=self.fund_name_dic[fund_id], linestyle='-', linewidth=2.5, color=line_color_list[i])
            for (i, fund_id) in enumerate(private_fund_list):
                plt.plot(fund_nav.index, fund_nav[fund_id], label=self.fund_name_dic[fund_id], linestyle='--', linewidth=2.5, color=line_color_list[i])
        plt.xticks(rotation=90)
        plt.xlabel('')
        plt.ylabel('')
        plt.legend(loc=2)
        plt.tight_layout()
        plt.savefig('{0}{1}.png'.format(self.data_path, self.comparison))
        fund_achievement = self.fund_achievement.copy(deep=True)
        fund_achievement.to_excel('{0}fund_achievement.xlsx'.format(self.data_path))
        fund_return_period = self.fund_return_period.copy(deep=True)
        fund_return_period.to_excel('{0}fund_return_period.xlsx'.format(self.data_path))
        fund_return_year = self.fund_return_year.copy(deep=True)
        fund_return_year.to_excel('{0}fund_return_year.xlsx'.format(self.data_path))
        fund_return_month = self.fund_return_month.copy(deep=True)
        fund_return_month.to_excel('{0}fund_return_month.xlsx'.format(self.data_path))
        fund_corr = self.fund_nav.pct_change().dropna().corr()
        fund_corr.columns = [self.fund_name_dic[i] for i in list(fund_corr.columns)]
        fund_corr.index = [self.fund_name_dic[i] for i in list(fund_corr.index)]
        fund_corr = fund_corr.reset_index()
        fund_corr['index'] = fund_corr['index'].astype('category')
        fund_corr['index'].cat.reorder_categories(self.rank_list, inplace=True)
        fund_corr = fund_corr.sort_values('index').set_index('index')
        fund_corr = fund_corr[self.rank_list]
        for i in range(len(fund_corr)):
            for j in range(len(fund_corr)):
                if i > j:
                    fund_corr.iloc[i, j] = np.nan
        fund_corr.to_excel('{0}corr.xlsx'.format(self.data_path))
        return
if __name__ == '__main__':
    start_date = '19900101'
    end_date = '20220915'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/performance/'
    comparison_list = ['朱雀', '个股精选（成长）', '个股精选（价值）', '中观轮动', '王斌相关']
    for comparison in comparison_list:
        if comparison == '朱雀':
            mutual_fund_list = ['007493']
            private_fund_list = ['P00016']
        elif comparison == '个股精选（成长）':
            mutual_fund_list = ['001856', '005827']
            private_fund_list = ['SEW532', 'SGS479']
        elif comparison == '个股精选（价值）':
            mutual_fund_list = ['002910', '688888']
            private_fund_list = ['SW5334', 'S66391']
        elif comparison == '中观轮动':
            mutual_fund_list = ['519002', '040035', '519126', '000739']
            private_fund_list = ['SES154', 'SY0344', 'SCP381', 'P20830']
        elif comparison == '王斌相关':
            mutual_fund_list = ['519002', '011251', '040035']
            private_fund_list = ['SES154', 'SY0344']
        else:
            mutual_fund_list = []
            private_fund_list = []
        Performance(comparison, start_date, end_date, data_path, mutual_fund_list, private_fund_list).get_result()
        print(comparison + ' finished !')