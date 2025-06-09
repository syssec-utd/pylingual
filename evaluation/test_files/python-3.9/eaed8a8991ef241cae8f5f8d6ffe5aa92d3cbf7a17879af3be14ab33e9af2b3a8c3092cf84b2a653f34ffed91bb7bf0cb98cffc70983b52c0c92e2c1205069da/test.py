import os
if os.path.exists('binance_f/privateconfig.py'):
    from binance_f.privateconfig import *
    g_api_key = p_api_key
    g_secret_key = p_secret_key
else:
    g_api_key = ''
    g_secret_key = ''
g_account_id = 12345678