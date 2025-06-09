"""
股票市场资金类指标
"""
import pandas as pd
from datetime import datetime
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
from WindPy import w
w.start()

class StockCashFlow:

    def __init__(self, start_date, end_date, is_increment=1):
        self.start_date = start_date
        self.end_date = end_date
        self.is_increment = is_increment
        self.table_name = 'mac_stock_cash_flow'

    def get_stock_cash_flow_data(self):
        """
        股票市场资金类数据：融资融券、北向资金
        """
        index_list = ['M0075992', 'M0075990', 'M0075991']
        name_dict = {'M0075992': 'margin', 'M0075990': 'financing', 'M0075991': 'sec_lending'}
        res = w.edb(','.join(index_list), self.start_date, self.end_date)
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print('fetch stock margin data error: start_date = {}, end_date = {}'.format(self.start_date, self.end_date))
        else:
            if len(res.Data) == 1:
                data = pd.DataFrame(res.Data[0], index=res.Codes, columns=res.Times).T
            else:
                data = pd.DataFrame(res.Data, index=res.Codes, columns=res.Times).T
            data.index.name = 'trade_date'
            data.reset_index(inplace=True)
            data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
            data.rename(columns=name_dict, inplace=True)
        margin = data.copy()
        res = w.wset('shhktransactionstatistics', 'startdate={};enddate={};cycle=day;currency=cny;field=date,sh_net_purchases'.format(self.start_date, self.end_date))
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print('fetch shhk data error: start_date = {}, end_date = {}'.format(self.start_date, self.end_date))
        else:
            data = pd.DataFrame(res.Data, index=res.Fields).T
            data.rename(columns={'date': 'trade_date'}, inplace=True)
            data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        shhk = data.copy()
        res = w.wset('szhktransactionstatistics', 'startdate={};enddate={};cycle=day;currency=cny;field=date,sz_net_purchases'.format(self.start_date, self.end_date))
        if res.ErrorCode != 0:
            data = pd.DataFrame()
            print('fetch szhk data error: start_date = {}, end_date = {}'.format(self.start_date, self.end_date))
        else:
            data = pd.DataFrame(res.Data, index=res.Fields).T
            data.rename(columns={'date': 'trade_date'}, inplace=True)
            data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        szhk = data.copy()
        hk_cash_df = pd.merge(shhk, szhk, on='trade_date', how='outer')
        cash_flow_df = margin.merge(hk_cash_df, on='trade_date', how='outer').sort_values(by='trade_date')
        return cash_flow_df

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.get_stock_cash_flow_data()
            sql_script = 'delete from {} where trade_date in ({})'.format(self.table_name, ','.join(data['trade_date'].tolist()))
            delete_duplicate_records(sql_script)
            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = '\n                    create table mac_stock_cash_flow(\n                    id int auto_increment primary key,\n                    trade_date date not null unique,\n                    margin decimal(10, 2),\n                    financing decimal(10, 2),\n                    sec_lending decimal(8, 2),\n                    sh_net_purchases decimal(6, 2),\n                    sz_net_purchases decimal(6, 2)) \n                '
            create_table(self.table_name, sql_script)
            data = self.get_stock_cash_flow_data()
            WriteToDB().write_to_db(data, self.table_name)
if __name__ == '__main__':
    StockCashFlow('2010-03-31', '2021-04-23', is_increment=0).get_construct_result()