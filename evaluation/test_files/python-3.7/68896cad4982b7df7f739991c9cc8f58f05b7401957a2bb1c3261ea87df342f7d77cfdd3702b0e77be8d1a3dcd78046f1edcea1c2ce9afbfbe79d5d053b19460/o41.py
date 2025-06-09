__author__ = 'ringo'
from tqsdk import TqApi, TqAuth
from tqsdk.ta import OPTION_IMPV
api = TqApi(auth=TqAuth('信易账户', '账户密码'))
quote = api.get_quote('SHFE.cu2006C50000')
klines = api.get_kline_serial(['SHFE.cu2006C50000', 'SHFE.cu2006'], 24 * 60 * 60, 20)
impv = OPTION_IMPV(klines, quote, 0.025)
print(list(impv['impv'] * 100))
api.close()