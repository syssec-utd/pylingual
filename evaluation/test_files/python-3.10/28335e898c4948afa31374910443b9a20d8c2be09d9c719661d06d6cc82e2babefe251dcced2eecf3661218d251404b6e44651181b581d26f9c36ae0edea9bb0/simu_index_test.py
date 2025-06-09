import hbshare as hbs
import pandas as pd
import time
if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)
    si = hbs.SimuIndex('RISK_MAX_DRAWDOWN_RANK_DAY', show_log=False)
    dt = si.get('S00748', '20210419', ['2101'])
    print(dt)
    cfg = si.get_config()
    indices = []
    for (index, row) in cfg.iterrows():
        if row['DAY']:
            indices.append((index + '_DAY', '日频_' + row['NAME_CN']))
        if row['WEEK']:
            indices.append((index + '_WEEK', '周频_' + row['NAME_CN']))
        if row['MONTH']:
            indices.append((index + '_MONTH', '月频_' + row['NAME_CN']))
        if row['YEAR']:
            indices.append((index + '_YEAR', '年频_' + row['NAME_CN']))
    print(indices)