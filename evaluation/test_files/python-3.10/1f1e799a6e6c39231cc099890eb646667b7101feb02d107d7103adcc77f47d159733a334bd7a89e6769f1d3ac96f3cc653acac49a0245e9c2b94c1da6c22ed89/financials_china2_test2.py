import os
os.chdir('S:/siat')
from siat.financials_china2 import *
tickers = ['000002.SZ', '600383.SS', '600048.SS', '600266.SS', '600606.SS', '000031.SZ']
fsdates = ['2021-12-31', '2020-12-31', '2019-12-31', '2018-12-31']
df = get_fin_stmt_ak_multi(tickers, fsdates)
ticker = '000002.SZ'
fsdate = '2021-12-31'
items1 = ['营业总收入', '营业总成本', '营业成本', '利润总额', '所得税费用', '净利润', '归母净利润']
dfp = fs_item_analysis_1(df, ticker, fsdate, items1)
dfs = find_fs_items(df, itemword1='费用', itemword2='')
dfs = find_fs_items(df, itemword1='损失', itemword2='')
dfs = find_fs_items(df, itemword1='总额', itemword2='')
items2 = ['营业总成本', '营业成本', '营业税金及附加', '销售费用', '管理费用', '研发费用', '应付利息', '公允价值变动损失', '资产处置损失', '资产处置损失', '资产减值损失', '营业外支出']
dfp2 = fs_item_analysis_1(df, '000002.SZ', '2021-12-31', items2)
fsdates1 = ['2021-12-31', '2020-12-31', '2019-12-31']
items3 = ['营业总成本', '营业总收入']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items3)
items4 = ['营业成本', '营业总成本']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items4)
items5 = ['营业成本', '营业总收入']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items5)
items6 = ['销售费用', '营业总收入']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items6)
items7 = ['管理费用', '营业总收入']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items7)
items8 = ['营业利润', '营业总收入']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items8)
items9 = ['净利润', '营业总收入']
dfp = fs_item_analysis_2(df, '000002.SZ', fsdates1, items9)
items8 = ['存货', '营业总收入']
dfp = asset_liab_analysis_2(df, '000002.SZ', fsdates1, items8)
dfs = find_fs_items(df, itemword1='流动', itemword2='')
dfp = asset_liab_analysis_3(df, '000002.SZ', fsdates1)
dfp = asset_liab_analysis_4(df, '000002.SZ', fsdates1)
dfp = asset_liab_analysis_5(df, '000002.SZ', fsdates1)
dfs = find_fs_items(df, itemword1='应收账款', itemword2='')
fsdates2 = ['2021-12-31', '2020-12-31']
items9 = ['应收账款', '营业收入']
dfp = asset_liab_analysis_6(df, '000002.SZ', fsdates2, items9)
items10 = ['存货', '营业收入']
dfp = asset_liab_analysis_6(df, '000002.SZ', fsdates2, items10)
items11 = ['存货', '资产总计', '存货占比%']
dfp = asset_liab_analysis_7(df, tickers, '2021-12-31', items11)
items12 = ['资产总计', '负债合计', '资产负债率%', '流动资产合计', '速动资产合计', '流动负债合计', '流动比率%', '速动比率%']
dfp = asset_liab_analysis_8(df, tickers, '2021-12-31', items12)
if __name__ == '__main__':
    asset_liab_structure(tickers, fsdates)