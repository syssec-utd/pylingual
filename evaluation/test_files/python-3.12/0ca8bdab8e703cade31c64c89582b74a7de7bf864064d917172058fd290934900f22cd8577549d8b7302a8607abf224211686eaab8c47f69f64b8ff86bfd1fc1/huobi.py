from ccxt.async_support.base.exchange import Exchange
import asyncio
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import AccountNotEnabled
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import NetworkError
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import OnMaintenance
from ccxt.base.errors import RequestTimeout
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise

class huobi(Exchange):

    def describe(self):
        return self.deep_extend(super(huobi, self).describe(), {'id': 'huobi', 'name': 'Huobi', 'countries': ['CN'], 'rateLimit': 100, 'userAgent': self.userAgents['chrome100'], 'certified': True, 'version': 'v1', 'accounts': None, 'accountsById': None, 'hostname': 'api.huobi.pro', 'pro': True, 'has': {'CORS': None, 'spot': True, 'margin': True, 'swap': True, 'future': True, 'option': None, 'addMargin': None, 'borrowMargin': True, 'cancelAllOrders': True, 'cancelOrder': True, 'cancelOrders': True, 'createDepositAddress': None, 'createOrder': True, 'createReduceOnlyOrder': False, 'createStopLimitOrder': True, 'createStopMarketOrder': True, 'createStopOrder': True, 'fetchAccounts': True, 'fetchBalance': True, 'fetchBidsAsks': None, 'fetchBorrowInterest': True, 'fetchBorrowRate': None, 'fetchBorrowRateHistories': None, 'fetchBorrowRateHistory': None, 'fetchBorrowRates': True, 'fetchBorrowRatesPerSymbol': True, 'fetchCanceledOrders': None, 'fetchClosedOrder': None, 'fetchClosedOrders': True, 'fetchCurrencies': True, 'fetchDeposit': None, 'fetchDepositAddress': True, 'fetchDepositAddresses': None, 'fetchDepositAddressesByNetwork': True, 'fetchDeposits': True, 'fetchFundingHistory': True, 'fetchFundingRate': True, 'fetchFundingRateHistory': True, 'fetchFundingRates': True, 'fetchIndexOHLCV': True, 'fetchL3OrderBook': None, 'fetchLedger': True, 'fetchLedgerEntry': None, 'fetchLeverage': False, 'fetchLeverageTiers': True, 'fetchMarketLeverageTiers': True, 'fetchMarkets': True, 'fetchMarkOHLCV': True, 'fetchMyBuys': None, 'fetchMySells': None, 'fetchMyTrades': True, 'fetchOHLCV': True, 'fetchOpenInterestHistory': True, 'fetchOpenOrder': None, 'fetchOpenOrders': True, 'fetchOrder': True, 'fetchOrderBook': True, 'fetchOrderBooks': None, 'fetchOrders': True, 'fetchOrderTrades': True, 'fetchPosition': True, 'fetchPositions': True, 'fetchPositionsRisk': False, 'fetchPremiumIndexOHLCV': True, 'fetchSettlementHistory': True, 'fetchStatus': True, 'fetchTicker': True, 'fetchTickers': True, 'fetchTime': True, 'fetchTrades': True, 'fetchTradingFee': True, 'fetchTradingFees': False, 'fetchTradingLimits': True, 'fetchTransactionFee': None, 'fetchTransactionFees': None, 'fetchTransactions': None, 'fetchTransfers': None, 'fetchWithdrawAddressesByNetwork': True, 'fetchWithdrawal': None, 'fetchWithdrawals': True, 'fetchWithdrawalWhitelist': None, 'reduceMargin': None, 'repayMargin': True, 'setLeverage': True, 'setMarginMode': False, 'setPositionMode': False, 'signIn': None, 'transfer': True, 'withdraw': True}, 'timeframes': {'1m': '1min', '5m': '5min', '15m': '15min', '30m': '30min', '1h': '60min', '4h': '4hour', '1d': '1day', '1w': '1week', '1M': '1mon', '1y': '1year'}, 'urls': {'logo': 'https://user-images.githubusercontent.com/1294454/76137448-22748a80-604e-11ea-8069-6e389271911d.jpg', 'hostnames': {'contract': 'api.hbdm.com', 'spot': 'api.huobi.pro', 'status': {'spot': 'status.huobigroup.com', 'future': {'inverse': 'status-dm.huobigroup.com', 'linear': 'status-linear-swap.huobigroup.com'}, 'swap': {'inverse': 'status-swap.huobigroup.com', 'linear': 'status-linear-swap.huobigroup.com'}}}, 'api': {'status': 'https://{hostname}', 'contract': 'https://{hostname}', 'spot': 'https://{hostname}', 'market': 'https://{hostname}', 'public': 'https://{hostname}', 'private': 'https://{hostname}', 'v2Public': 'https://{hostname}', 'v2Private': 'https://{hostname}'}, 'www': 'https://www.huobi.com', 'referral': {'url': 'https://www.huobi.com/en-us/topic/double-reward/?invite_code=6rmm2223', 'discount': 0.15}, 'doc': ['https://huobiapi.github.io/docs/spot/v1/cn/', 'https://huobiapi.github.io/docs/dm/v1/cn/', 'https://huobiapi.github.io/docs/coin_margined_swap/v1/cn/', 'https://huobiapi.github.io/docs/usdt_swap/v1/cn/', 'https://huobiapi.github.io/docs/option/v1/cn/'], 'fees': 'https://www.huobi.com/about/fee/'}, 'api': {'v2Public': {'get': {'reference/currencies': 1, 'market-status': 1}}, 'v2Private': {'get': {'account/ledger': 1, 'account/withdraw/quota': 1, 'account/withdraw/address': 1, 'account/deposit/address': 1, 'account/repayment': 5, 'reference/transact-fee-rate': 1, 'account/asset-valuation': 0.2, 'point/account': 5, 'sub-user/user-list': 1, 'sub-user/user-state': 1, 'sub-user/account-list': 1, 'sub-user/deposit-address': 1, 'sub-user/query-deposit': 1, 'user/api-key': 1, 'user/uid': 1, 'algo-orders/opening': 1, 'algo-orders/history': 1, 'algo-orders/specific': 1, 'c2c/offers': 1, 'c2c/offer': 1, 'c2c/transactions': 1, 'c2c/repayment': 1, 'c2c/account': 1, 'etp/reference': 1, 'etp/transactions': 5, 'etp/transaction': 5, 'etp/rebalance': 1, 'etp/limit': 1}, 'post': {'account/transfer': 1, 'account/repayment': 5, 'point/transfer': 5, 'sub-user/management': 1, 'sub-user/creation': 1, 'sub-user/tradable-market': 1, 'sub-user/transferability': 1, 'sub-user/api-key-generation': 1, 'sub-user/api-key-modification': 1, 'sub-user/api-key-deletion': 1, 'sub-user/deduct-mode': 1, 'algo-orders': 1, 'algo-orders/cancel-all-after': 1, 'algo-orders/cancellation': 1, 'c2c/offer': 1, 'c2c/cancellation': 1, 'c2c/cancel-all': 1, 'c2c/repayment': 1, 'c2c/transfer': 1, 'etp/creation': 5, 'etp/redemption': 5, 'etp/{transactId}/cancel': 10, 'etp/batch-cancel': 50}}, 'market': {'get': {'history/kline': 1, 'detail/merged': 1, 'depth': 1, 'trade': 1, 'history/trade': 1, 'detail': 1, 'tickers': 1, 'etp': 1}}, 'public': {'get': {'common/symbols': 1, 'common/currencys': 1, 'common/timestamp': 1, 'common/exchange': 1, 'settings/currencys': 1}}, 'private': {'get': {'account/accounts': 0.2, 'account/accounts/{id}/balance': 0.2, 'account/accounts/{sub-uid}': 1, 'account/history': 4, 'cross-margin/loan-info': 1, 'margin/loan-info': 1, 'fee/fee-rate/get': 1, 'order/openOrders': 0.4, 'order/orders': 0.4, 'order/orders/{id}': 0.4, 'order/orders/{id}/matchresults': 0.4, 'order/orders/getClientOrder': 0.4, 'order/history': 1, 'order/matchresults': 1, 'query/deposit-withdraw': 1, 'margin/loan-orders': 0.2, 'margin/accounts/balance': 0.2, 'cross-margin/loan-orders': 1, 'cross-margin/accounts/balance': 1, 'points/actions': 1, 'points/orders': 1, 'subuser/aggregate-balance': 10, 'stable-coin/exchange_rate': 1, 'stable-coin/quote': 1}, 'post': {'account/transfer': 1, 'futures/transfer': 1, 'order/batch-orders': 0.4, 'order/orders/place': 0.2, 'order/orders/submitCancelClientOrder': 0.2, 'order/orders/batchCancelOpenOrders': 0.4, 'order/orders/{id}/submitcancel': 0.2, 'order/orders/batchcancel': 0.4, 'dw/withdraw/api/create': 1, 'dw/withdraw-virtual/{id}/cancel': 1, 'dw/transfer-in/margin': 10, 'dw/transfer-out/margin': 10, 'margin/orders': 10, 'margin/orders/{id}/repay': 10, 'cross-margin/transfer-in': 1, 'cross-margin/transfer-out': 1, 'cross-margin/orders': 1, 'cross-margin/orders/{id}/repay': 1, 'stable-coin/exchange': 1, 'subuser/transfer': 10}}, 'status': {'public': {'spot': {'get': {'api/v2/summary.json': 1}}, 'future': {'inverse': {'get': {'api/v2/summary.json': 1}}, 'linear': {'get': {'api/v2/summary.json': 1}}}, 'swap': {'inverse': {'get': {'api/v2/summary.json': 1}}, 'linear': {'get': {'api/v2/summary.json': 1}}}}}, 'spot': {'public': {'get': {'v2/market-status': 1, 'v1/common/symbols': 1, 'v1/common/currencys': 1, 'v2/reference/currencies': 1, 'v1/common/timestamp': 1, 'v1/common/exchange': 1, 'market/history/candles': 1, 'market/history/kline': 1, 'market/detail/merged': 1, 'market/tickers': 1, 'market/depth': 1, 'market/trade': 1, 'market/history/trade': 1, 'market/detail/': 1, 'market/etp': 1, 'v2/etp/reference': 1, 'v2/etp/rebalance': 1}}, 'private': {'get': {'v1/account/accounts': 0.2, 'v1/account/accounts/{account-id}/balance': 0.2, 'v2/account/valuation': 1, 'v2/account/asset-valuation': 0.2, 'v1/account/history': 4, 'v2/account/ledger': 1, 'v2/point/account': 5, 'v2/account/deposit/address': 1, 'v2/account/withdraw/quota': 1, 'v2/account/withdraw/address': 1, 'v2/reference/currencies': 1, 'v1/query/deposit-withdraw': 1, 'v2/user/api-key': 1, 'v2/user/uid': 1, 'v2/sub-user/user-list': 1, 'v2/sub-user/user-state': 1, 'v2/sub-user/account-list': 1, 'v2/sub-user/deposit-address': 1, 'v2/sub-user/query-deposit': 1, 'v1/subuser/aggregate-balance': 10, 'v1/account/accounts/{sub-uid}': 1, 'v1/order/openOrders': 0.4, 'v1/order/orders/{order-id}': 0.4, 'v1/order/orders/getClientOrder': 0.4, 'v1/order/orders/{order-id}/matchresults': 0.4, 'v1/order/orders': 0.4, 'v1/order/history': 1, 'v1/order/matchresults': 1, 'v2/reference/transact-fee-rate': 1, 'v2/algo-orders/opening': 1, 'v2/algo-orders/history': 1, 'v2/algo-orders/specific': 1, 'v1/margin/loan-info': 1, 'v1/margin/loan-orders': 0.2, 'v1/margin/accounts/balance': 0.2, 'v1/cross-margin/loan-info': 1, 'v1/cross-margin/loan-orders': 1, 'v1/cross-margin/accounts/balance': 1, 'v2/account/repayment': 5, 'v1/stable-coin/quote': 1, 'v2/etp/transactions': 5, 'v2/etp/transaction': 5, 'v2/etp/limit': 1}, 'post': {'v1/account/transfer': 1, 'v1/futures/transfer': 1, 'v2/point/transfer': 5, 'v2/account/transfer': 1, 'v1/dw/withdraw/api/create': 1, 'v1/dw/withdraw-virtual/{withdraw-id}/cancel': 1, 'v2/sub-user/deduct-mode': 1, 'v2/sub-user/creation': 1, 'v2/sub-user/management': 1, 'v2/sub-user/tradable-market': 1, 'v2/sub-user/transferability': 1, 'v2/sub-user/api-key-generation': 1, 'v2/sub-user/api-key-modification': 1, 'v2/sub-user/api-key-deletion': 1, 'v1/subuser/transfer': 10, 'v1/order/orders/place': 0.2, 'v1/order/batch-orders': 0.4, 'v1/order/orders/{order-id}/submitcancel': 0.2, 'v1/order/orders/submitCancelClientOrder': 0.2, 'v1/order/orders/batchCancelOpenOrders': 0.4, 'v1/order/orders/batchcancel': 0.4, 'v2/algo-orders/cancel-all-after': 1, 'v2/algo-orders': 1, 'v2/algo-orders/cancellation': 1, 'v2/account/repayment': 5, 'v1/dw/transfer-in/margin': 10, 'v1/dw/transfer-out/margin': 10, 'v1/margin/orders': 10, 'v1/margin/orders/{order-id}/repay': 10, 'v1/cross-margin/transfer-in': 1, 'v1/cross-margin/transfer-out': 1, 'v1/cross-margin/orders': 1, 'v1/cross-margin/orders/{order-id}/repay': 1, 'v1/stable-coin/exchange': 1, 'v2/etp/creation': 5, 'v2/etp/redemption': 5, 'v2/etp/{transactId}/cancel': 10, 'v2/etp/batch-cancel': 50}}}, 'contract': {'public': {'get': {'api/v1/timestamp': 1, 'heartbeat/': 1, 'api/v1/contract_contract_info': 1, 'api/v1/contract_index': 1, 'api/v1/contract_price_limit': 1, 'api/v1/contract_open_interest': 1, 'api/v1/contract_delivery_price': 1, 'market/depth': 1, 'market/bbo': 1, 'market/history/kline': 1, 'index/market/history/mark_price_kline': 1, 'market/detail/merged': 1, 'market/detail/batch_merged': 1, 'market/trade': 1, 'market/history/trade': 1, 'api/v1/contract_risk_info': 1, 'api/v1/contract_insurance_fund': 1, 'api/v1/contract_adjustfactor': 1, 'api/v1/contract_his_open_interest': 1, 'api/v1/contract_ladder_margin': 1, 'api/v1/contract_api_state': 1, 'api/v1/contract_elite_account_ratio': 1, 'api/v1/contract_elite_position_ratio': 1, 'api/v1/contract_liquidation_orders': 1, 'api/v1/contract_settlement_records': 1, 'index/market/history/index': 1, 'index/market/history/basis': 1, 'api/v1/contract_estimated_settlement_price': 1, 'swap-api/v1/swap_contract_info': 1, 'swap-api/v1/swap_index': 1, 'swap-api/v1/swap_price_limit': 1, 'swap-api/v1/swap_open_interest': 1, 'swap-ex/market/depth': 1, 'swap-ex/market/bbo': 1, 'swap-ex/market/history/kline': 1, 'index/market/history/swap_mark_price_kline': 1, 'swap-ex/market/detail/merged': 1, 'swap-ex/market/detail/batch_merged': 1, 'swap-ex/market/trade': 1, 'swap-ex/market/history/trade': 1, 'swap-api/v1/swap_risk_info': 1, 'swap-api/v1/swap_insurance_fund': 1, 'swap-api/v1/swap_adjustfactor': 1, 'swap-api/v1/swap_his_open_interest': 1, 'swap-api/v1/swap_ladder_margin': 1, 'swap-api/v1/swap_api_state': 1, 'swap-api/v1/swap_elite_account_ratio': 1, 'swap-api/v1/swap_elite_position_ratio': 1, 'swap-api/v1/swap_estimated_settlement_price': 1, 'swap-api/v1/swap_liquidation_orders': 1, 'swap-api/v1/swap_settlement_records': 1, 'swap-api/v1/swap_funding_rate': 1, 'swap-api/v1/swap_batch_funding_rate': 1, 'swap-api/v1/swap_historical_funding_rate': 1, 'index/market/history/swap_premium_index_kline': 1, 'index/market/history/swap_estimated_rate_kline': 1, 'index/market/history/swap_basis': 1, 'linear-swap-api/v1/swap_contract_info': 1, 'linear-swap-api/v1/swap_index': 1, 'linear-swap-api/v1/swap_price_limit': 1, 'linear-swap-api/v1/swap_open_interest': 1, 'linear-swap-ex/market/depth': 1, 'linear-swap-ex/market/bbo': 1, 'linear-swap-ex/market/history/kline': 1, 'index/market/history/linear_swap_mark_price_kline': 1, 'linear-swap-ex/market/detail/merged': 1, 'linear-swap-ex/market/detail/batch_merged': 1, 'linear-swap-ex/market/trade': 1, 'linear-swap-ex/market/history/trade': 1, 'linear-swap-api/v1/swap_risk_info': 1, 'swap-api/v1/linear-swap-api/v1/swap_insurance_fund': 1, 'linear-swap-api/v1/swap_adjustfactor': 1, 'linear-swap-api/v1/swap_cross_adjustfactor': 1, 'linear-swap-api/v1/swap_his_open_interest': 1, 'linear-swap-api/v1/swap_ladder_margin': 1, 'linear-swap-api/v1/swap_cross_ladder_margin': 1, 'linear-swap-api/v1/swap_api_state': 1, 'linear-swap-api/v1/swap_cross_transfer_state': 1, 'linear-swap-api/v1/swap_cross_trade_state': 1, 'linear-swap-api/v1/swap_elite_account_ratio': 1, 'linear-swap-api/v1/swap_elite_position_ratio': 1, 'linear-swap-api/v1/swap_liquidation_orders': 1, 'linear-swap-api/v1/swap_settlement_records': 1, 'linear-swap-api/v1/swap_funding_rate': 1, 'linear-swap-api/v1/swap_batch_funding_rate': 1, 'linear-swap-api/v1/swap_historical_funding_rate': 1, 'index/market/history/linear_swap_premium_index_kline': 1, 'index/market/history/linear_swap_estimated_rate_kline': 1, 'index/market/history/linear_swap_basis': 1, 'linear-swap-api/v1/swap_estimated_settlement_price': 1}}, 'private': {'get': {'api/v1/contract_api_trading_status': 1, 'swap-api/v1/swap_api_trading_status': 1, 'linear-swap-api/v1/swap_api_trading_status': 1}, 'post': {'api/v1/contract_balance_valuation': 1, 'api/v1/contract_account_info': 1, 'api/v1/contract_position_info': 1, 'api/v1/contract_sub_auth': 1, 'api/v1/contract_sub_account_list': 1, 'api/v1/contract_sub_account_info_list': 1, 'api/v1/contract_sub_account_info': 1, 'api/v1/contract_sub_position_info': 1, 'api/v1/contract_financial_record': 1, 'api/v1/contract_financial_record_exact': 1, 'api/v1/contract_user_settlement_records': 1, 'api/v1/contract_order_limit': 1, 'api/v1/contract_fee': 1, 'api/v1/contract_transfer_limit': 1, 'api/v1/contract_position_limit': 1, 'api/v1/contract_account_position_info': 1, 'api/v1/contract_master_sub_transfer': 1, 'api/v1/contract_master_sub_transfer_record': 1, 'api/v1/contract_available_level_rate': 1, 'api/v1/contract_order': 1, 'v1/contract_batchorder': 1, 'api/v1/contract_cancel': 1, 'api/v1/contract_cancelall': 1, 'api/v1/contract_switch_lever_rate': 1, 'api/v1/lightning_close_position': 1, 'api/v1/contract_order_info': 1, 'api/v1/contract_order_detail': 1, 'api/v1/contract_openorders': 1, 'api/v1/contract_hisorders': 1, 'api/v1/contract_hisorders_exact': 1, 'api/v1/contract_matchresults': 1, 'api/v1/contract_matchresults_exact': 1, 'api/v1/contract_trigger_order': 1, 'api/v1/contract_trigger_cancel': 1, 'api/v1/contract_trigger_cancelall': 1, 'api/v1/contract_trigger_openorders': 1, 'api/v1/contract_trigger_hisorders': 1, 'api/v1/contract_tpsl_order': 1, 'api/v1/contract_tpsl_cancel': 1, 'api/v1/contract_tpsl_cancelall': 1, 'api/v1/contract_tpsl_openorders': 1, 'api/v1/contract_tpsl_hisorders': 1, 'api/v1/contract_relation_tpsl_order': 1, 'api/v1/contract_track_order': 1, 'api/v1/contract_track_cancel': 1, 'api/v1/contract_track_cancelall': 1, 'api/v1/contract_track_openorders': 1, 'api/v1/contract_track_hisorders': 1, 'swap-api/v1/swap_balance_valuation': 1, 'swap-api/v1/swap_account_info': 1, 'swap-api/v1/swap_position_info': 1, 'swap-api/v1/swap_account_position_info': 1, 'swap-api/v1/swap_sub_auth': 1, 'swap-api/v1/swap_sub_account_list': 1, 'swap-api/v1/swap_sub_account_info_list': 1, 'swap-api/v1/swap_sub_account_info': 1, 'swap-api/v1/swap_sub_position_info': 1, 'swap-api/v1/swap_financial_record': 1, 'swap-api/v1/swap_financial_record_exact': 1, 'swap-api/v1/swap_user_settlement_records': 1, 'swap-api/v1/swap_available_level_rate': 1, 'swap-api/v1/swap_order_limit': 1, 'swap-api/v1/swap_fee': 1, 'swap-api/v1/swap_transfer_limit': 1, 'swap-api/v1/swap_position_limit': 1, 'swap-api/v1/swap_master_sub_transfer': 1, 'swap-api/v1/swap_master_sub_transfer_record': 1, 'swap-api/v1/swap_order': 1, 'swap-api/v1/swap_batchorder': 1, 'swap-api/v1/swap_cancel': 1, 'swap-api/v1/swap_cancelall': 1, 'swap-api/v1/swap_lightning_close_position': 1, 'swap-api/v1/swap_switch_lever_rate': 1, 'swap-api/v1/swap_order_info': 1, 'swap-api/v1/swap_order_detail': 1, 'swap-api/v1/swap_openorders': 1, 'swap-api/v1/swap_hisorders': 1, 'swap-api/v1/swap_hisorders_exact': 1, 'swap-api/v1/swap_matchresults': 1, 'swap-api/v1/swap_matchresults_exact': 1, 'swap-api/v1/swap_trigger_order': 1, 'swap-api/v1/swap_trigger_cancel': 1, 'swap-api/v1/swap_trigger_cancelall': 1, 'swap-api/v1/swap_trigger_openorders': 1, 'swap-api/v1/swap_trigger_hisorders': 1, 'swap-api/v1/swap_tpsl_order': 1, 'swap-api/v1/swap_tpsl_cancel': 1, 'swap-api/v1/swap_tpsl_cancelall': 1, 'swap-api/v1/swap_tpsl_openorders': 1, 'swap-api/v1/swap_tpsl_hisorders': 1, 'swap-api/v1/swap_relation_tpsl_order': 1, 'swap-api/v1/swap_track_order': 1, 'swap-api/v1/swap_track_cancel': 1, 'swap-api/v1/swap_track_cancelall': 1, 'swap-api/v1/swap_track_openorders': 1, 'swap-api/v1/swap_track_hisorders': 1, 'linear-swap-api/v1/swap_lever_position_limit': 1, 'linear-swap-api/v1/swap_cross_lever_position_limit': 1, 'linear-swap-api/v1/swap_balance_valuation': 1, 'linear-swap-api/v1/swap_account_info': 1, 'linear-swap-api/v1/swap_cross_account_info': 1, 'linear-swap-api/v1/swap_position_info': 1, 'linear-swap-api/v1/swap_cross_position_info': 1, 'linear-swap-api/v1/swap_account_position_info': 1, 'linear-swap-api/v1/swap_cross_account_position_info': 1, 'linear-swap-api/v1/swap_sub_auth': 1, 'linear-swap-api/v1/swap_sub_account_list': 1, 'linear-swap-api/v1/swap_cross_sub_account_list': 1, 'linear-swap-api/v1/swap_sub_account_info_list': 1, 'linear-swap-api/v1/swap_cross_sub_account_info_list': 1, 'linear-swap-api/v1/swap_sub_account_info': 1, 'linear-swap-api/v1/swap_cross_sub_account_info': 1, 'linear-swap-api/v1/swap_sub_position_info': 1, 'linear-swap-api/v1/swap_cross_sub_position_info': 1, 'linear-swap-api/v1/swap_financial_record': 1, 'linear-swap-api/v1/swap_financial_record_exact': 1, 'linear-swap-api/v1/swap_user_settlement_records': 1, 'linear-swap-api/v1/swap_cross_user_settlement_records': 1, 'linear-swap-api/v1/swap_available_level_rate': 1, 'linear-swap-api/v1/swap_cross_available_level_rate': 1, 'linear-swap-api/v1/swap_order_limit': 1, 'linear-swap-api/v1/swap_fee': 1, 'linear-swap-api/v1/swap_transfer_limit': 1, 'linear-swap-api/v1/swap_cross_transfer_limit': 1, 'linear-swap-api/v1/swap_position_limit': 1, 'linear-swap-api/v1/swap_cross_position_limit': 1, 'linear-swap-api/v1/swap_master_sub_transfer': 1, 'linear-swap-api/v1/swap_master_sub_transfer_record': 1, 'linear-swap-api/v1/swap_transfer_inner': 1, 'linear-swap-api/v1/swap_order': 1, 'linear-swap-api/v1/swap_cross_order': 1, 'linear-swap-api/v1/swap_batchorder': 1, 'linear-swap-api/v1/swap_cross_batchorder': 1, 'linear-swap-api/v1/swap_cancel': 1, 'linear-swap-api/v1/swap_cross_cancel': 1, 'linear-swap-api/v1/swap_cancelall': 1, 'linear-swap-api/v1/swap_cross_cancelall': 1, 'linear-swap-api/v1/swap_switch_lever_rate': 1, 'linear-swap-api/v1/swap_cross_switch_lever_rate': 1, 'linear-swap-api/v1/swap_lightning_close_position': 1, 'linear-swap-api/v1/swap_cross_lightning_close_position': 1, 'linear-swap-api/v1/swap_order_info': 1, 'linear-swap-api/v1/swap_cross_order_info': 1, 'linear-swap-api/v1/swap_order_detail': 1, 'linear-swap-api/v1/swap_cross_order_detail': 1, 'linear-swap-api/v1/swap_openorders': 1, 'linear-swap-api/v1/swap_cross_openorders': 1, 'linear-swap-api/v1/swap_hisorders': 1, 'linear-swap-api/v1/swap_cross_hisorders': 1, 'linear-swap-api/v1/swap_hisorders_exact': 1, 'linear-swap-api/v1/swap_cross_hisorders_exact': 1, 'linear-swap-api/v1/swap_matchresults': 1, 'linear-swap-api/v1/swap_cross_matchresults': 1, 'linear-swap-api/v1/swap_matchresults_exact': 1, 'linear-swap-api/v1/swap_cross_matchresults_exact': 1, 'linear-swap-api/v1/swap_switch_position_mode': 1, 'linear-swap-api/v1/swap_cross_switch_position_mode': 1, 'linear-swap-api/v1/swap_trigger_order': 1, 'linear-swap-api/v1/swap_cross_trigger_order': 1, 'linear-swap-api/v1/swap_trigger_cancel': 1, 'linear-swap-api/v1/swap_cross_trigger_cancel': 1, 'linear-swap-api/v1/swap_trigger_cancelall': 1, 'linear-swap-api/v1/swap_cross_trigger_cancelall': 1, 'linear-swap-api/v1/swap_trigger_openorders': 1, 'linear-swap-api/v1/swap_cross_trigger_openorders': 1, 'linear-swap-api/v1/swap_trigger_hisorders': 1, 'linear-swap-api/v1/swap_cross_trigger_hisorders': 1, 'linear-swap-api/v1/swap_tpsl_order': 1, 'linear-swap-api/v1/swap_cross_tpsl_order': 1, 'linear-swap-api/v1/swap_tpsl_cancel': 1, 'linear-swap-api/v1/swap_cross_tpsl_cancel': 1, 'linear-swap-api/v1/swap_tpsl_cancelall': 1, 'linear-swap-api/v1/swap_cross_tpsl_cancelall': 1, 'linear-swap-api/v1/swap_tpsl_openorders': 1, 'linear-swap-api/v1/swap_cross_tpsl_openorders': 1, 'linear-swap-api/v1/swap_tpsl_hisorders': 1, 'linear-swap-api/v1/swap_cross_tpsl_hisorders': 1, 'linear-swap-api/v1/swap_relation_tpsl_order': 1, 'linear-swap-api/v1/swap_cross_relation_tpsl_order': 1, 'linear-swap-api/v1/swap_track_order': 1, 'linear-swap-api/v1/swap_cross_track_order': 1, 'linear-swap-api/v1/swap_track_cancel': 1, 'linear-swap-api/v1/swap_cross_track_cancel': 1, 'linear-swap-api/v1/swap_track_cancelall': 1, 'linear-swap-api/v1/swap_cross_track_cancelall': 1, 'linear-swap-api/v1/swap_track_openorders': 1, 'linear-swap-api/v1/swap_cross_track_openorders': 1, 'linear-swap-api/v1/swap_track_hisorders': 1, 'linear-swap-api/v1/swap_cross_track_hisorders': 1}}}}, 'fees': {'trading': {'feeSide': 'get', 'tierBased': False, 'percentage': True, 'maker': self.parse_number('0.002'), 'taker': self.parse_number('0.002')}}, 'exceptions': {'broad': {'contract is restricted of closing positions on API.  Please contact customer service': OnMaintenance, 'maintain': OnMaintenance}, 'exact': {'403': AuthenticationError, '1010': AccountNotEnabled, '1013': BadSymbol, '1017': OrderNotFound, '1034': InvalidOrder, '1036': InvalidOrder, '1039': InvalidOrder, '1041': InvalidOrder, '1047': InsufficientFunds, '1048': InsufficientFunds, '1051': InvalidOrder, '1066': BadSymbol, '1067': InvalidOrder, '1094': InvalidOrder, '1220': AccountNotEnabled, '1461': InvalidOrder, 'bad-request': BadRequest, 'validation-format-error': BadRequest, 'validation-constraints-required': BadRequest, 'base-date-limit-error': BadRequest, 'api-not-support-temp-addr': PermissionDenied, 'timeout': RequestTimeout, 'gateway-internal-error': ExchangeNotAvailable, 'account-frozen-balance-insufficient-error': InsufficientFunds, 'invalid-amount': InvalidOrder, 'order-limitorder-amount-min-error': InvalidOrder, 'order-limitorder-amount-max-error': InvalidOrder, 'order-marketorder-amount-min-error': InvalidOrder, 'order-limitorder-price-min-error': InvalidOrder, 'order-limitorder-price-max-error': InvalidOrder, 'order-invalid-price': InvalidOrder, 'order-holding-limit-failed': InvalidOrder, 'order-orderprice-precision-error': InvalidOrder, 'order-etp-nav-price-max-error': InvalidOrder, 'order-orderstate-error': OrderNotFound, 'order-queryorder-invalid': OrderNotFound, 'order-update-error': ExchangeNotAvailable, 'api-signature-check-failed': AuthenticationError, 'api-signature-not-valid': AuthenticationError, 'base-record-invalid': OrderNotFound, 'base-symbol-trade-disabled': BadSymbol, 'base-symbol-error': BadSymbol, 'system-maintenance': OnMaintenance, 'base-request-exceed-frequency-limit': RateLimitExceeded, 'invalid symbol': BadSymbol, 'symbol trade not open now': BadSymbol, 'require-symbol': BadSymbol, 'invalid-address': BadRequest, 'base-currency-chain-error': BadRequest, 'dw-insufficient-balance': InsufficientFunds}}, 'precisionMode': TICK_SIZE, 'options': {'fetchMarkets': {'types': {'spot': True, 'future': {'linear': True, 'inverse': True}, 'swap': {'linear': True, 'inverse': True}}}, 'defaultType': 'spot', 'defaultSubType': 'inverse', 'defaultNetwork': 'ERC20', 'networks': {'ETH': 'erc20', 'TRX': 'trc20', 'HRC20': 'hrc20', 'HECO': 'hrc20', 'HT': 'hrc20', 'ALGO': 'algo', 'OMNI': ''}, 'fetchOrdersByStatesMethod': 'spot_private_get_v1_order_orders', 'createMarketBuyOrderRequiresPrice': True, 'language': 'en-US', 'broker': {'id': 'AA03022abc'}, 'accountsByType': {'spot': 'pro', 'funding': 'pro', 'future': 'futures'}, 'accountsById': {'spot': 'spot', 'margin': 'margin', 'otc': 'otc', 'point': 'point', 'super-margin': 'super-margin', 'investment': 'investment', 'borrow': 'borrow', 'grid-trading': 'grid-trading', 'deposit-earning': 'deposit-earning', 'otc-options': 'otc-options'}, 'marginAccounts': {'cross': 'super-margin', 'isolated': 'margin'}, 'typesByAccount': {'pro': 'spot', 'futures': 'future'}, 'spot': {'stopOrderTypes': {'stop-limit': True, 'buy-stop-limit': True, 'sell-stop-limit': True, 'stop-limit-fok': True, 'buy-stop-limit-fok': True, 'sell-stop-limit-fok': True}, 'limitOrderTypes': {'limit': True, 'buy-limit': True, 'sell-limit': True, 'ioc': True, 'buy-ioc': True, 'sell-ioc': True, 'limit-maker': True, 'buy-limit-maker': True, 'sell-limit-maker': True, 'stop-limit': True, 'buy-stop-limit': True, 'sell-stop-limit': True, 'limit-fok': True, 'buy-limit-fok': True, 'sell-limit-fok': True, 'stop-limit-fok': True, 'buy-stop-limit-fok': True, 'sell-stop-limit-fok': True}}}, 'commonCurrencies': {'GET': 'Themis', 'GTC': 'Game.com', 'HIT': 'HitChain', 'HOT': 'Hydro Protocol', 'PNT': 'Penta', 'SBTC': 'Super Bitcoin', 'BIFI': 'Bitcoin File'}})

    async def fetch_status(self, params={}):
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchMyTrades', None, params)
        method = 'statusPublicSpotGetApiV2SummaryJson'
        if marketType != 'spot':
            subType = self.safe_string(params, 'subType', self.options['defaultSubType'])
            if marketType == 'swap':
                if subType == 'linear':
                    method = 'statusPublicSwapLinearGetApiV2SummaryJson'
                elif subType == 'inverse':
                    method = 'statusPublicSwapInverseGetApiV2SummaryJson'
            elif marketType == 'future':
                if subType == 'linear':
                    method = 'statusPublicFutureLinearGetApiV2SummaryJson'
                elif subType == 'inverse':
                    method = 'statusPublicFutureInverseGetApiV2SummaryJson'
            elif marketType == 'contract':
                method = 'contractPublicGetHeartbeat'
        response = await getattr(self, method)()
        status = None
        updated = None
        url = None
        if method == 'contractPublicGetHeartbeat':
            statusRaw = self.safe_string(response, 'status')
            status = 'ok' if statusRaw == 'ok' else 'maintenance'
            updated = self.safe_string(response, 'ts')
        else:
            statusData = self.safe_value(response, 'status', {})
            statusRaw = self.safe_string(statusData, 'indicator')
            status = 'ok' if statusRaw == 'none' else 'maintenance'
            pageData = self.safe_value(response, 'page', {})
            datetime = self.safe_string(pageData, 'updated_at')
            updated = self.parse8601(datetime)
            url = self.safe_string(pageData, 'url')
        return {'status': status, 'updated': updated, 'eta': None, 'url': url, 'info': response}

    async def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        options = self.safe_value(self.options, 'fetchTime', {})
        defaultType = self.safe_string(self.options, 'defaultType', 'spot')
        type = self.safe_string(options, 'type', defaultType)
        type = self.safe_string(params, 'type', type)
        method = 'spotPublicGetV1CommonTimestamp'
        if type == 'future' or type == 'swap':
            method = 'contractPublicGetApiV1Timestamp'
        response = await getattr(self, method)(params)
        return self.safe_integer_2(response, 'data', 'ts')

    def parse_trading_fee(self, fee, market=None):
        marketId = self.safe_string(fee, 'symbol')
        return {'info': fee, 'symbol': self.safe_symbol(marketId, market), 'maker': self.safe_number(fee, 'actualMakerRate'), 'taker': self.safe_number(fee, 'actualTakerRate')}

    async def fetch_trading_fee(self, symbol, params={}):
        """
        fetch the trading fees for a market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `fee structure <https://docs.ccxt.com/en/latest/manual.html#fee-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {'symbols': market['id']}
        response = await self.spotPrivateGetV2ReferenceTransactFeeRate(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        first = self.safe_value(data, 0, {})
        return self.parse_trading_fee(first, market)

    async def fetch_trading_limits(self, symbols=None, params={}):
        await self.load_markets()
        if symbols is None:
            symbols = self.symbols
        result = {}
        for i in range(0, len(symbols)):
            symbol = symbols[i]
            result[symbol] = await self.fetch_trading_limits_by_id(self.market_id(symbol), params)
        return result

    async def fetch_trading_limits_by_id(self, id, params={}):
        request = {'symbol': id}
        response = await self.spotPublicGetV1CommonExchange(self.extend(request, params))
        return self.parse_trading_limits(self.safe_value(response, 'data', {}))

    def parse_trading_limits(self, limits, symbol=None, params={}):
        return {'info': limits, 'limits': {'amount': {'min': self.safe_number(limits, 'limit-order-must-greater-than'), 'max': self.safe_number(limits, 'limit-order-must-less-than')}}}

    def cost_to_precision(self, symbol, cost):
        return self.decimal_to_precision(cost, TRUNCATE, self.markets[symbol]['precision']['cost'], self.precisionMode)

    async def fetch_markets(self, params={}):
        """
        retrieves data on all markets for huobi
        :param dict params: extra parameters specific to the exchange api endpoint
        :returns [dict]: an array of objects representing market data
        """
        options = self.safe_value(self.options, 'fetchMarkets', {})
        types = self.safe_value(options, 'types', {})
        allMarkets = []
        promises = []
        keys = list(types.keys())
        for i in range(0, len(keys)):
            type = keys[i]
            value = self.safe_value(types, type)
            if value is True:
                promises.append(self.fetch_markets_by_type_and_sub_type(type, None, params))
            else:
                subKeys = list(value.keys())
                for j in range(0, len(subKeys)):
                    subType = subKeys[j]
                    subValue = self.safe_value(value, subType)
                    if subValue:
                        promises.append(self.fetch_markets_by_type_and_sub_type(type, subType, params))
        promises = await asyncio.gather(*promises)
        for i in range(0, len(promises)):
            allMarkets = self.array_concat(allMarkets, promises[i])
        return allMarkets

    async def fetch_markets_by_type_and_sub_type(self, type, subType, params={}):
        method = 'spotPublicGetV1CommonSymbols'
        query = self.omit(params, ['type', 'subType'])
        spot = type == 'spot'
        contract = type != 'spot'
        future = type == 'future'
        swap = type == 'swap'
        linear = None
        inverse = None
        request = {}
        if contract:
            linear = subType == 'linear'
            inverse = subType == 'inverse'
            if linear:
                method = 'contractPublicGetLinearSwapApiV1SwapContractInfo'
                if future:
                    request['business_type'] = 'futures'
            elif inverse:
                if future:
                    method = 'contractPublicGetApiV1ContractContractInfo'
                elif swap:
                    method = 'contractPublicGetSwapApiV1SwapContractInfo'
        response = await getattr(self, method)(self.extend(request, query))
        markets = self.safe_value(response, 'data', [])
        numMarkets = len(markets)
        if numMarkets < 1:
            raise NetworkError(self.id + ' fetchMarkets() returned an empty response: ' + self.json(markets))
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            baseId = None
            quoteId = None
            settleId = None
            id = None
            lowercaseId = None
            lowercaseBaseId = None
            if contract:
                id = self.safe_string(market, 'contract_code')
                lowercaseId = id.lower()
                if swap:
                    parts = id.split('-')
                    baseId = self.safe_string(market, 'symbol')
                    lowercaseBaseId = baseId.lower()
                    quoteId = self.safe_string_lower(parts, 1)
                    settleId = baseId if inverse else quoteId
                elif future:
                    baseId = self.safe_string(market, 'symbol')
                    lowercaseBaseId = baseId.lower()
                    if inverse:
                        quoteId = 'USD'
                        settleId = baseId
                    else:
                        pair = self.safe_string(market, 'pair')
                        parts = pair.split('-')
                        quoteId = self.safe_string(parts, 1)
                        settleId = quoteId
            else:
                baseId = self.safe_string(market, 'base-currency')
                lowercaseBaseId = baseId.lower()
                quoteId = self.safe_string(market, 'quote-currency')
                id = baseId + quoteId
                lowercaseId = id.lower()
            base = self.safe_currency_code(baseId)
            quote = self.safe_currency_code(quoteId)
            settle = self.safe_currency_code(settleId)
            symbol = base + '/' + quote
            expiry = None
            if contract:
                if inverse:
                    symbol += ':' + base
                elif linear:
                    symbol += ':' + quote
                if future:
                    expiry = self.safe_integer(market, 'delivery_time')
                    symbol += '-' + self.yymmdd(expiry)
            contractSize = self.safe_number(market, 'contract_size')
            pricePrecision = None
            amountPrecision = None
            costPrecision = None
            if spot:
                pricePrecision = self.safe_string(market, 'price-precision')
                pricePrecision = self.parse_number('1e-' + pricePrecision)
                amountPrecision = self.safe_string(market, 'amount-precision')
                amountPrecision = self.parse_number('1e-' + amountPrecision)
                costPrecision = self.safe_string(market, 'value-precision')
                costPrecision = self.parse_number('1e-' + costPrecision)
            else:
                pricePrecision = self.safe_number(market, 'price_tick')
                amountPrecision = 1
            maker = None
            taker = None
            if spot:
                maker = 0 if base == 'OMG' else 0.2 / 100
                taker = 0 if base == 'OMG' else 0.2 / 100
            minAmount = self.safe_number(market, 'min-order-amt')
            maxAmount = self.safe_number(market, 'max-order-amt')
            minCost = self.safe_number(market, 'min-order-value', 0)
            active = None
            if spot:
                state = self.safe_string(market, 'state')
                active = state == 'online'
            elif contract:
                contractStatus = self.safe_integer(market, 'contract_status')
                active = contractStatus == 1
            leverageRatio = self.safe_string(market, 'leverage-ratio', '1')
            superLeverageRatio = self.safe_string(market, 'super-margin-leverage-ratio', '1')
            hasLeverage = Precise.string_gt(leverageRatio, '1') or Precise.string_gt(superLeverageRatio, '1')
            result.append({'id': id, 'lowercaseId': lowercaseId, 'symbol': symbol, 'base': base, 'quote': quote, 'settle': settle, 'baseId': baseId, 'lowercaseBaseId': lowercaseBaseId, 'quoteId': quoteId, 'settleId': settleId, 'type': type, 'spot': spot, 'margin': spot and hasLeverage, 'swap': swap, 'future': future, 'option': False, 'active': active, 'contract': contract, 'linear': linear, 'inverse': inverse, 'taker': taker, 'maker': maker, 'contractSize': contractSize, 'expiry': expiry, 'expiryDatetime': self.iso8601(expiry), 'strike': None, 'optionType': None, 'precision': {'amount': amountPrecision, 'price': pricePrecision, 'cost': costPrecision}, 'limits': {'leverage': {'min': self.parse_number('1'), 'max': self.parse_number(leverageRatio), 'superMax': self.parse_number(superLeverageRatio)}, 'amount': {'min': minAmount, 'max': maxAmount}, 'price': {'min': None, 'max': None}, 'cost': {'min': minCost, 'max': None}}, 'info': market})
        return result

    def parse_ticker(self, ticker, market=None):
        marketId = self.safe_string_2(ticker, 'symbol', 'contract_code')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.safe_integer(ticker, 'ts')
        bid = None
        bidVolume = None
        ask = None
        askVolume = None
        if 'bid' in ticker:
            if isinstance(ticker['bid'], list):
                bid = self.safe_string(ticker['bid'], 0)
                bidVolume = self.safe_string(ticker['bid'], 1)
            else:
                bid = self.safe_string(ticker, 'bid')
                bidVolume = self.safe_string(ticker, 'bidSize')
        if 'ask' in ticker:
            if isinstance(ticker['ask'], list):
                ask = self.safe_string(ticker['ask'], 0)
                askVolume = self.safe_string(ticker['ask'], 1)
            else:
                ask = self.safe_string(ticker, 'ask')
                askVolume = self.safe_string(ticker, 'askSize')
        open = self.safe_string(ticker, 'open')
        close = self.safe_string(ticker, 'close')
        baseVolume = self.safe_string(ticker, 'amount')
        quoteVolume = self.safe_string(ticker, 'vol')
        return self.safe_ticker({'symbol': symbol, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'high': self.safe_string(ticker, 'high'), 'low': self.safe_string(ticker, 'low'), 'bid': bid, 'bidVolume': bidVolume, 'ask': ask, 'askVolume': askVolume, 'vwap': None, 'open': open, 'close': close, 'last': close, 'previousClose': None, 'change': None, 'percentage': None, 'average': None, 'baseVolume': baseVolume, 'quoteVolume': quoteVolume, 'info': ticker}, market)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        fieldName = 'symbol'
        method = 'spotPublicGetMarketDetailMerged'
        if market['linear']:
            method = 'contractPublicGetLinearSwapExMarketDetailMerged'
            fieldName = 'contract_code'
        elif market['inverse']:
            if market['future']:
                method = 'contractPublicGetMarketDetailMerged'
            elif market['swap']:
                method = 'contractPublicGetSwapExMarketDetailMerged'
                fieldName = 'contract_code'
        request[fieldName] = market['id']
        response = await getattr(self, method)(self.extend(request, params))
        tick = self.safe_value(response, 'tick', {})
        ticker = self.parse_ticker(tick, market)
        timestamp = self.safe_integer(response, 'ts')
        ticker['timestamp'] = timestamp
        ticker['datetime'] = self.iso8601(timestamp)
        return ticker

    async def fetch_tickers(self, symbols=None, params={}):
        """
        fetches price tickers for multiple markets, statistical calculations with the information calculated over the past 24 hours each market
        :param [str]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: an array of `ticker structures <https://docs.ccxt.com/en/latest/manual.html#ticker-structure>`
        """
        await self.load_markets()
        options = self.safe_value(self.options, 'fetchTickers', {})
        defaultType = self.safe_string(self.options, 'defaultType', 'spot')
        type = self.safe_string(options, 'type', defaultType)
        type = self.safe_string(params, 'type', type)
        method = 'spotPublicGetMarketTickers'
        defaultSubType = self.safe_string(self.options, 'defaultSubType', 'inverse')
        subType = self.safe_string(options, 'subType', defaultSubType)
        subType = self.safe_string(params, 'subType', subType)
        request = {}
        future = type == 'future'
        swap = type == 'swap'
        linear = subType == 'linear'
        inverse = subType == 'inverse'
        if future or swap:
            if linear:
                method = 'contractPublicGetLinearSwapExMarketDetailBatchMerged'
                if future:
                    request['business_type'] = 'futures'
            elif inverse:
                if future:
                    method = 'contractPublicGetMarketDetailBatchMerged'
                elif swap:
                    method = 'contractPublicGetSwapExMarketDetailBatchMerged'
        params = self.omit(params, ['type', 'subType'])
        response = await getattr(self, method)(self.extend(request, params))
        tickers = self.safe_value_2(response, 'data', 'ticks', [])
        timestamp = self.safe_integer(response, 'ts')
        result = {}
        for i in range(0, len(tickers)):
            ticker = self.parse_ticker(tickers[i])
            if future and linear:
                for j in range(0, len(self.symbols)):
                    symbol = self.symbols[j]
                    market = self.market(symbol)
                    contractType = self.safe_string(market['info'], 'contract_type')
                    if contractType == 'this_week' and ticker['symbol'] == market['baseId'] + '-' + market['quoteId'] + '-CW':
                        ticker['symbol'] = market['symbol']
                        break
                    elif contractType == 'next_week' and ticker['symbol'] == market['baseId'] + '-' + market['quoteId'] + '-NW':
                        ticker['symbol'] = market['symbol']
                        break
                    elif contractType == 'this_quarter' and ticker['symbol'] == market['baseId'] + '-' + market['quoteId'] + '-CQ':
                        ticker['symbol'] = market['symbol']
                        break
                    elif contractType == 'next_quarter' and ticker['symbol'] == market['baseId'] + '-' + market['quoteId'] + '-NQ':
                        ticker['symbol'] = market['symbol']
                        break
            symbol = ticker['symbol']
            ticker['timestamp'] = timestamp
            ticker['datetime'] = self.iso8601(timestamp)
            result[symbol] = ticker
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/en/latest/manual.html#order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {'type': 'step0'}
        fieldName = 'symbol'
        method = 'spotPublicGetMarketDepth'
        if market['linear']:
            method = 'contractPublicGetLinearSwapExMarketDepth'
            fieldName = 'contract_code'
        elif market['inverse']:
            if market['future']:
                method = 'contractPublicGetMarketDepth'
            elif market['swap']:
                method = 'contractPublicGetSwapExMarketDepth'
                fieldName = 'contract_code'
        elif limit is not None:
            if limit != 5 and limit != 10 and (limit != 20) and (limit != 150):
                raise BadRequest(self.id + ' fetchOrderBook() limit argument must be None, 5, 10, 20, or 150, default is 150')
            if limit != 150:
                request['depth'] = limit
        request[fieldName] = market['id']
        response = await getattr(self, method)(self.extend(request, params))
        if 'tick' in response:
            if not response['tick']:
                raise BadSymbol(self.id + ' fetchOrderBook() returned empty response: ' + self.json(response))
            tick = self.safe_value(response, 'tick')
            timestamp = self.safe_integer(tick, 'ts', self.safe_integer(response, 'ts'))
            result = self.parse_order_book(tick, symbol, timestamp)
            result['nonce'] = self.safe_integer(tick, 'version')
            return result
        raise ExchangeError(self.id + ' fetchOrderBook() returned unrecognized response: ' + self.json(response))

    def parse_trade(self, trade, market=None):
        marketId = self.safe_string_2(trade, 'contract_code', 'symbol')
        market = self.safe_market(marketId, market)
        symbol = market['symbol']
        timestamp = self.safe_integer_2(trade, 'ts', 'created-at')
        timestamp = self.safe_integer_2(trade, 'created_at', 'create_date', timestamp)
        order = self.safe_string_2(trade, 'order-id', 'order_id')
        side = self.safe_string(trade, 'direction')
        type = self.safe_string(trade, 'type')
        if type is not None:
            typeParts = type.split('-')
            side = typeParts[0]
            type = typeParts[1]
        takerOrMaker = self.safe_string_lower(trade, 'role')
        priceString = self.safe_string_2(trade, 'price', 'trade_price')
        amountString = self.safe_string_2(trade, 'filled-amount', 'amount')
        amountString = self.safe_string(trade, 'trade_volume', amountString)
        costString = self.safe_string(trade, 'trade_turnover')
        fee = None
        feeCost = self.safe_string_2(trade, 'filled-fees', 'trade_fee')
        feeCurrencyId = self.safe_string_2(trade, 'fee-currency', 'fee_asset')
        feeCurrency = self.safe_currency_code(feeCurrencyId)
        filledPoints = self.safe_string(trade, 'filled-points')
        if filledPoints is not None:
            if feeCost is None or Precise.string_equals(feeCost, '0'):
                feeDeductCurrency = self.safe_string(trade, 'fee-deduct-currency')
                if feeDeductCurrency != '':
                    feeCost = filledPoints
                    feeCurrency = self.safe_currency_code(feeDeductCurrency)
        if feeCost is not None:
            fee = {'cost': feeCost, 'currency': feeCurrency}
        tradeId = self.safe_string_2(trade, 'trade-id', 'tradeId')
        id = self.safe_string_2(trade, 'trade_id', 'id', tradeId)
        return self.safe_trade({'id': id, 'info': trade, 'order': order, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'symbol': symbol, 'type': type, 'side': side, 'takerOrMaker': takerOrMaker, 'price': priceString, 'amount': amountString, 'cost': costString, 'fee': fee}, market)

    async def fetch_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        """
        fetch all the trades made from a single order
        :param str id: order id
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchOrderTrades', None, params)
        method = self.get_supported_mapping(marketType, {'spot': 'fetchSpotOrderTrades'})
        return await getattr(self, method)(id, symbol, since, limit, params)

    async def fetch_spot_order_trades(self, id, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        request = {'order-id': id}
        response = await self.spotPrivateGetV1OrderOrdersOrderIdMatchresults(self.extend(request, params))
        return self.parse_trades(response['data'], None, since, limit)

    async def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all trades made by the user
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch trades for
        :param int|None limit: the maximum number of trades structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html#trade-structure>`
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchMyTrades', None, params)
        request = {}
        method = None
        market = None
        if marketType == 'spot':
            if symbol is not None:
                market = self.market(symbol)
                request['symbol'] = market['id']
            if limit is not None:
                request['size'] = limit
            if since is not None:
                request['start-time'] = since
            method = 'spotPrivateGetV1OrderMatchresults'
        else:
            if symbol is None:
                raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol for ' + marketType + ' orders')
            market = self.market(symbol)
            request['contract_code'] = market['id']
            request['trade_type'] = 0
            if market['linear']:
                defaultMargin = 'cross' if market['future'] else 'isolated'
                marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
                if marginMode == 'isolated':
                    method = 'contractPrivatePostLinearSwapApiV1SwapMatchresultsExact'
                elif marginMode == 'cross':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCrossMatchresultsExact'
            elif market['inverse']:
                if marketType == 'future':
                    method = 'contractPrivatePostApiV1ContractMatchresultsExact'
                    request['symbol'] = market['settleId']
                elif marketType == 'swap':
                    method = 'contractPrivatePostSwapApiV1SwapMatchresultsExact'
                else:
                    raise NotSupported(self.id + ' fetchMyTrades() does not support ' + marketType + ' markets')
        response = await getattr(self, method)(self.extend(request, params))
        trades = self.safe_value(response, 'data')
        if not isinstance(trades, list):
            trades = self.safe_value(trades, 'trades')
        return self.parse_trades(trades, market, since, limit)

    async def fetch_trades(self, symbol, since=None, limit=1000, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {}
        fieldName = 'symbol'
        method = 'spotPublicGetMarketHistoryTrade'
        if market['future']:
            if market['inverse']:
                method = 'contractPublicGetMarketHistoryTrade'
            elif market['linear']:
                method = 'contractPublicGetLinearSwapExMarketHistoryTrade'
                fieldName = 'contract_code'
        elif market['swap']:
            if market['inverse']:
                method = 'contractPublicGetSwapExMarketHistoryTrade'
            elif market['linear']:
                method = 'contractPublicGetLinearSwapExMarketHistoryTrade'
            fieldName = 'contract_code'
        request[fieldName] = market['id']
        if limit is not None:
            request['size'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        result = []
        for i in range(0, len(data)):
            trades = self.safe_value(data[i], 'data', [])
            for j in range(0, len(trades)):
                trade = self.parse_trade(trades[j], market)
                result.append(trade)
        result = self.sort_by(result, 'timestamp')
        return self.filter_by_symbol_since_limit(result, market['symbol'], since, limit)

    def parse_ohlcv(self, ohlcv, market=None):
        return [self.safe_timestamp(ohlcv, 'id'), self.safe_number(ohlcv, 'open'), self.safe_number(ohlcv, 'high'), self.safe_number(ohlcv, 'low'), self.safe_number(ohlcv, 'close'), self.safe_number(ohlcv, 'amount')]

    async def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int|None since: timestamp in ms of the earliest candle to fetch
        :param int|None limit: the maximum amount of candles to fetch
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [[int]]: A list of candles ordered as timestamp, open, high, low, close, volume
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {'period': self.timeframes[timeframe]}
        fieldName = 'symbol'
        price = self.safe_string(params, 'price')
        params = self.omit(params, 'price')
        method = 'spotPublicGetMarketHistoryCandles'
        if market['spot']:
            if since is not None:
                request['from'] = int(since / 1000)
            if limit is not None:
                request['size'] = limit
        elif market['future']:
            if market['inverse']:
                if price == 'mark':
                    method = 'contractPublicGetIndexMarketHistoryMarkPriceKline'
                elif price == 'index':
                    method = 'contractPublicGetIndexMarketHistoryIndex'
                elif price == 'premiumIndex':
                    raise BadRequest(self.id + ' ' + market['type'] + ' has no api endpoint for ' + price + ' kline data')
                else:
                    method = 'contractPublicGetMarketHistoryKline'
            elif market['linear']:
                if price == 'mark':
                    method = 'contractPublicGetIndexMarketHistoryLinearSwapMarkPriceKline'
                elif price == 'index':
                    raise BadRequest(self.id + ' ' + market['type'] + ' has no api endpoint for ' + price + ' kline data')
                elif price == 'premiumIndex':
                    method = 'contractPublicGetIndexMarketHistoryLinearSwapPremiumIndexKline'
                else:
                    method = 'contractPublicGetLinearSwapExMarketHistoryKline'
                fieldName = 'contract_code'
        elif market['swap']:
            if market['inverse']:
                if price == 'mark':
                    method = 'contractPublicGetIndexMarketHistorySwapMarkPriceKline'
                elif price == 'index':
                    raise BadRequest(self.id + ' ' + market['type'] + ' has no api endpoint for ' + price + ' kline data')
                elif price == 'premiumIndex':
                    method = 'contractPublicGetIndexMarketHistorySwapPremiumIndexKline'
                else:
                    method = 'contractPublicGetSwapExMarketHistoryKline'
            elif market['linear']:
                if price == 'mark':
                    method = 'contractPublicGetIndexMarketHistoryLinearSwapMarkPriceKline'
                elif price == 'index':
                    raise BadRequest(self.id + ' ' + market['type'] + ' has no api endpoint for ' + price + ' kline data')
                elif price == 'premiumIndex':
                    method = 'contractPublicGetIndexMarketHistoryLinearSwapPremiumIndexKline'
                else:
                    method = 'contractPublicGetLinearSwapExMarketHistoryKline'
            fieldName = 'contract_code'
        if market['contract']:
            if limit is None:
                limit = 2000
            request['size'] = limit
            if price is None:
                duration = self.parse_timeframe(timeframe)
                if since is None:
                    now = self.seconds()
                    request['from'] = now - duration * (limit - 1)
                    request['to'] = now
                else:
                    start = int(since / 1000)
                    request['from'] = start
                    request['to'] = self.sum(start, duration * (limit - 1))
        request[fieldName] = market['id']
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    async def fetch_accounts(self, params={}):
        """
        fetch all the accounts associated with a profile
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a dictionary of `account structures <https://docs.ccxt.com/en/latest/manual.html#account-structure>` indexed by the account type
        """
        await self.load_markets()
        response = await self.spotPrivateGetV1AccountAccounts(params)
        data = self.safe_value(response, 'data')
        return self.parse_accounts(data)

    def parse_account(self, account):
        typeId = self.safe_string(account, 'type')
        accountsById = self.safe_value(self.options, 'accountsById', {})
        type = self.safe_value(accountsById, typeId, typeId)
        return {'info': account, 'id': self.safe_string(account, 'id'), 'type': type, 'code': None}

    async def fetch_account_id_by_type(self, type, params={}):
        accounts = await self.load_accounts()
        accountId = self.safe_value(params, 'account-id')
        if accountId is not None:
            return accountId
        indexedAccounts = self.index_by(accounts, 'type')
        defaultAccount = self.safe_value(accounts, 0, {})
        account = self.safe_value(indexedAccounts, type, defaultAccount)
        return self.safe_string(account, 'id')

    async def fetch_currencies(self, params={}):
        """
        fetches all available currencies on an exchange
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = await self.spotPublicGetV2ReferenceCurrencies(params)
        data = self.safe_value(response, 'data', [])
        result = {}
        for i in range(0, len(data)):
            entry = data[i]
            currencyId = self.safe_string(entry, 'currency')
            code = self.safe_currency_code(currencyId)
            chains = self.safe_value(entry, 'chains', [])
            networks = {}
            instStatus = self.safe_string(entry, 'instStatus')
            currencyActive = instStatus == 'normal'
            fee = None
            minPrecision = None
            minWithdraw = None
            maxWithdraw = None
            deposit = None
            withdraw = None
            for j in range(0, len(chains)):
                chain = chains[j]
                networkId = self.safe_string(chain, 'chain')
                baseChainProtocol = self.safe_string(chain, 'baseChainProtocol')
                huobiToken = 'h' + currencyId
                if baseChainProtocol is None:
                    if huobiToken == networkId:
                        baseChainProtocol = 'ERC20'
                    else:
                        baseChainProtocol = self.safe_string(chain, 'displayName')
                network = self.safe_network(baseChainProtocol)
                minWithdraw = self.safe_number(chain, 'minWithdrawAmt')
                maxWithdraw = self.safe_number(chain, 'maxWithdrawAmt')
                withdrawStatus = self.safe_string(chain, 'withdrawStatus')
                depositStatus = self.safe_string(chain, 'depositStatus')
                withdrawEnabled = withdrawStatus == 'allowed'
                depositEnabled = depositStatus == 'allowed'
                active = withdrawEnabled and depositEnabled
                precision = self.safe_string(chain, 'withdrawPrecision')
                if precision is not None:
                    precision = self.parse_number('1e-' + precision)
                    minPrecision = precision if minPrecision is None else max(precision, minPrecision)
                if withdrawEnabled and (not withdraw):
                    withdraw = True
                elif not withdrawEnabled:
                    withdraw = False
                if depositEnabled and (not deposit):
                    deposit = True
                elif not depositEnabled:
                    deposit = False
                fee = self.safe_number(chain, 'transactFeeWithdraw')
                networks[network] = {'info': chain, 'id': networkId, 'network': network, 'limits': {'withdraw': {'min': minWithdraw, 'max': maxWithdraw}}, 'active': active, 'deposit': depositEnabled, 'withdraw': withdrawEnabled, 'fee': fee, 'precision': precision}
            networksKeys = list(networks.keys())
            networkLength = len(networksKeys)
            result[code] = {'info': entry, 'code': code, 'id': currencyId, 'active': currencyActive, 'deposit': deposit, 'withdraw': withdraw, 'fee': fee if networkLength <= 1 else None, 'name': None, 'limits': {'amount': {'min': None, 'max': None}, 'withdraw': {'min': minWithdraw if networkLength <= 1 else None, 'max': maxWithdraw if networkLength <= 1 else None}}, 'precision': minPrecision, 'networks': networks}
        return result

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        type = None
        type, params = self.handle_market_type_and_params('fetchBalance', None, params)
        options = self.safe_value(self.options, 'fetchBalance', {})
        request = {}
        method = None
        margin = type == 'margin'
        spot = type == 'spot'
        future = type == 'future'
        swap = type == 'swap'
        defaultSubType = self.safe_string_2(self.options, 'defaultSubType', 'subType', 'inverse')
        subType = self.safe_string_2(options, 'defaultSubType', 'subType', defaultSubType)
        subType = self.safe_string_2(params, 'defaultSubType', 'subType', subType)
        inverse = subType == 'inverse'
        linear = subType == 'linear'
        marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', 'isolated')
        marginMode = self.safe_string_2(options, 'defaultMarginMode', 'marginMode', marginMode)
        marginMode = self.safe_string_2(params, 'defaultMarginMode', 'marginMode', marginMode)
        params = self.omit(params, ['defaultSubType', 'subType', 'defaultMarginMode', 'marginMode'])
        isolated = marginMode == 'isolated'
        cross = marginMode == 'cross'
        if spot:
            await self.load_accounts()
            accountId = await self.fetch_account_id_by_type(type, params)
            request['account-id'] = accountId
            method = 'spotPrivateGetV1AccountAccountsAccountIdBalance'
        elif margin:
            if isolated:
                method = 'spotPrivateGetV1MarginAccountsBalance'
            elif cross:
                method = 'spotPrivateGetV1CrossMarginAccountsBalance'
        elif linear:
            if isolated:
                method = 'contractPrivatePostLinearSwapApiV1SwapAccountInfo'
            elif cross:
                method = 'contractPrivatePostLinearSwapApiV1SwapCrossAccountInfo'
        elif inverse:
            if future:
                method = 'contractPrivatePostApiV1ContractAccountInfo'
            elif swap:
                method = 'contractPrivatePostSwapApiV1SwapAccountInfo'
        response = await getattr(self, method)(self.extend(request, params))
        result = {'info': response}
        data = self.safe_value(response, 'data')
        if spot or margin:
            balances = self.safe_value(data, 'list', [])
            for i in range(0, len(balances)):
                balance = balances[i]
                currencyId = self.safe_string(balance, 'currency')
                code = self.safe_currency_code(currencyId)
                account = None
                if code in result:
                    account = result[code]
                else:
                    account = self.account()
                if balance['type'] == 'trade':
                    account['free'] = self.safe_string(balance, 'balance')
                if balance['type'] == 'frozen':
                    account['used'] = self.safe_string(balance, 'balance')
                result[code] = account
        elif linear:
            first = self.safe_value(data, 0, {})
            if cross:
                account = self.account()
                account['free'] = self.safe_string(first, 'margin_balance', 'margin_available')
                account['used'] = self.safe_string(first, 'margin_frozen')
                currencyId = self.safe_string_2(first, 'margin_asset', 'symbol')
                code = self.safe_currency_code(currencyId)
                result[code] = account
            elif isolated:
                for i in range(0, len(data)):
                    balance = data[i]
                    marketId = self.safe_string_2(balance, 'contract_code', 'margin_account')
                    market = self.safe_market(marketId)
                    currencyId = self.safe_string(balance, 'margin_asset')
                    currency = self.safe_currency(currencyId)
                    code = self.safe_string(market, 'settle', currency['code'])
                    if code is not None:
                        account = self.account()
                        account['free'] = self.safe_string(balance, 'margin_balance')
                        account['used'] = self.safe_string(balance, 'margin_frozen')
                        accountsByCode = {}
                        accountsByCode[code] = account
                        symbol = market['symbol']
                        result[symbol] = self.safe_balance(accountsByCode)
                return result
        elif inverse:
            for i in range(0, len(data)):
                balance = data[i]
                currencyId = self.safe_string(balance, 'symbol')
                code = self.safe_currency_code(currencyId)
                account = self.account()
                account['free'] = self.safe_string(balance, 'margin_available')
                account['used'] = self.safe_string(balance, 'margin_frozen')
                result[code] = account
        return self.safe_balance(result)

    async def fetch_order(self, id, symbol=None, params={}):
        """
        fetches information on an order made by the user
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchOrder', None, params)
        request = {}
        method = None
        market = None
        if marketType == 'spot':
            clientOrderId = self.safe_string(params, 'clientOrderId')
            method = 'spotPrivateGetV1OrderOrdersOrderId'
            if clientOrderId is not None:
                method = 'spotPrivateGetV1OrderOrdersGetClientOrder'
            else:
                request['order-id'] = id
        else:
            if symbol is None:
                raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol for ' + marketType + ' orders')
            market = self.market(symbol)
            request['contract_code'] = market['id']
            if market['linear']:
                defaultMargin = 'cross' if market['future'] else 'isolated'
                marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
                if marginMode == 'isolated':
                    method = 'contractPrivatePostLinearSwapApiV1SwapOrderInfo'
                elif marginMode == 'cross':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCrossOrderInfo'
            elif market['inverse']:
                if marketType == 'future':
                    method = 'contractPrivatePostApiV1ContractOrderInfo'
                    request['symbol'] = market['settleId']
                elif marketType == 'swap':
                    method = 'contractPrivatePostSwapApiV1SwapOrderInfo'
                else:
                    raise NotSupported(self.id + ' fetchOrder() does not support ' + marketType + ' markets')
            clientOrderId = self.safe_string_2(params, 'client_order_id', 'clientOrderId')
            if clientOrderId is None:
                request['order_id'] = id
            else:
                request['client_order_id'] = clientOrderId
                params = self.omit(params, ['client_order_id', 'clientOrderId'])
        response = await getattr(self, method)(self.extend(request, params))
        order = self.safe_value(response, 'data')
        if isinstance(order, list):
            order = self.safe_value(order, 0)
        return self.parse_order(order)

    async def fetch_spot_orders_by_states(self, states, symbol=None, since=None, limit=None, params={}):
        method = self.safe_string(self.options, 'fetchOrdersByStatesMethod', 'spot_private_get_v1_order_orders')
        if method == 'spot_private_get_v1_order_orders':
            if symbol is None:
                raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        await self.load_markets()
        market = None
        request = {'states': states}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        if since is not None:
            request['start-time'] = since
            request['end-time'] = self.sum(since, 48 * 60 * 60 * 1000)
        if limit is not None:
            request['size'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_orders(data, market, since, limit)

    async def fetch_spot_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_spot_orders_by_states('pre-submitted,submitted,partial-filled,filled,partial-canceled,canceled', symbol, since, limit, params)

    async def fetch_closed_spot_orders(self, symbol=None, since=None, limit=None, params={}):
        return await self.fetch_spot_orders_by_states('filled,partial-canceled,canceled', symbol, since, limit, params)

    async def fetch_contract_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchContractOrders() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchOrders', market, params)
        request = {'contract_code': market['id'], 'trade_type': 0, 'type': 1, 'status': '0', 'create_date': 90}
        method = None
        request['contract_code'] = market['id']
        if market['linear']:
            defaultMargin = 'cross' if market['future'] else 'isolated'
            marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
            method = self.get_supported_mapping(marginMode, {'isolated': 'contractPrivatePostLinearSwapApiV1SwapHisorders', 'cross': 'contractPrivatePostLinearSwapApiV1SwapCrossHisorders'})
        elif market['inverse']:
            method = self.get_supported_mapping(marketType, {'future': 'contractPrivatePostApiV1ContractHisorders', 'swap': 'contractPrivatePostSwapApiV1SwapHisorders'})
            if marketType == 'future':
                request['symbol'] = market['settleId']
        if limit is not None:
            request['page_size'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        orders = self.safe_value(data, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    async def fetch_closed_contract_orders(self, symbol=None, since=None, limit=None, params={}):
        request = {'status': '5,6,7'}
        return await self.fetch_contract_orders(symbol, since, limit, self.extend(request, params))

    async def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of [order structures]{@link https://docs.ccxt.com/en/latest/manual.html#order-structure
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchOrders', None, params)
        method = self.get_supported_mapping(marketType, {'spot': 'fetchSpotOrders', 'swap': 'fetchContractOrders', 'future': 'fetchContractOrders'})
        if method is None:
            raise NotSupported(self.id + ' fetchOrders() does not support ' + marketType + ' markets yet')
        contract = marketType == 'swap' or marketType == 'future'
        if contract and symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument for ' + marketType + ' orders')
        return await getattr(self, method)(symbol, since, limit, params)

    async def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches information on multiple closed orders made by the user
        :param str|None symbol: unified market symbol of the market orders were made in
        :param int|None since: the earliest time in ms to fetch orders for
        :param int|None limit: the maximum number of  orde structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of [order structures]{@link https://docs.ccxt.com/en/latest/manual.html#order-structure
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchClosedOrders', None, params)
        method = self.get_supported_mapping(marketType, {'spot': 'fetchClosedSpotOrders', 'swap': 'fetchClosedContractOrders', 'future': 'fetchClosedContractOrders'})
        if method is None:
            raise NotSupported(self.id + ' fetchClosedOrders() does not support ' + marketType + ' markets yet')
        return await getattr(self, method)(symbol, since, limit, params)

    async def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch all unfilled currently open orders
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch open orders for
        :param int|None limit: the maximum number of  open orders structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchOpenOrders', None, params)
        request = {}
        method = None
        market = None
        if marketType == 'spot':
            method = 'spotPrivateGetV1OrderOpenOrders'
            if symbol is not None:
                market = self.market(symbol)
                request['symbol'] = market['id']
            accountId = self.safe_string(params, 'account-id')
            if accountId is None:
                await self.load_accounts()
                for i in range(0, len(self.accounts)):
                    account = self.accounts[i]
                    if account['type'] == 'spot':
                        accountId = self.safe_string(account, 'id')
                        if accountId is not None:
                            break
            request['account-id'] = accountId
            if limit is not None:
                request['size'] = limit
            params = self.omit(params, 'account-id')
        else:
            if symbol is None:
                raise ArgumentsRequired(self.id + ' fetchOpenOrders() requires a symbol for ' + marketType + ' orders')
            market = self.market(symbol)
            request['contract_code'] = market['id']
            if market['linear']:
                defaultMargin = 'cross' if market['future'] else 'isolated'
                marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
                if marginMode == 'isolated':
                    method = 'contractPrivatePostLinearSwapApiV1SwapOpenorders'
                elif marginMode == 'cross':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCrossOpenorders'
            elif market['inverse']:
                if market['future']:
                    method = 'contractPrivatePostApiV1ContractOpenorders'
                    request['symbol'] = market['settleId']
                elif market['swap']:
                    method = 'contractPrivatePostSwapApiV1SwapOpenorders'
            if limit is not None:
                request['page_size'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        orders = self.safe_value(response, 'data')
        if not isinstance(orders, list):
            orders = self.safe_value(orders, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    def parse_order_status(self, status):
        statuses = {'partial-filled': 'open', 'partial-canceled': 'canceled', 'filled': 'closed', 'canceled': 'canceled', 'submitted': 'open', 'created': 'open', '1': 'open', '2': 'open', '3': 'open', '4': 'open', '5': 'canceled', '6': 'closed', '7': 'canceled', '11': 'canceling'}
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string_2(order, 'id', 'order_id_str')
        side = self.safe_string(order, 'direction')
        type = self.safe_string(order, 'order_price_type')
        if 'type' in order:
            orderType = order['type'].split('-')
            side = orderType[0]
            type = orderType[1]
        status = self.parse_order_status(self.safe_string_2(order, 'state', 'status'))
        marketId = self.safe_string_2(order, 'contract_code', 'symbol')
        market = self.safe_market(marketId, market)
        timestamp = self.safe_integer_n(order, ['created_at', 'created-at', 'create_date'])
        clientOrderId = self.safe_string_2(order, 'client_order_id', 'client-order-id')
        amount = self.safe_string_2(order, 'volume', 'amount')
        filled = self.safe_string_2(order, 'filled-amount', 'field-amount')
        filled = self.safe_string(order, 'trade_volume', filled)
        price = self.safe_string(order, 'price')
        cost = self.safe_string_2(order, 'filled-cash-amount', 'field-cash-amount')
        cost = self.safe_string(order, 'trade_turnover', cost)
        feeCost = self.safe_string_2(order, 'filled-fees', 'field-fees')
        feeCost = self.safe_string(order, 'fee', feeCost)
        fee = None
        if feeCost is not None:
            feeCurrency = None
            feeCurrencyId = self.safe_string(order, 'fee_asset')
            if feeCurrencyId is not None:
                feeCurrency = self.safe_currency_code(feeCurrencyId)
            else:
                feeCurrency = market['quote'] if side == 'sell' else market['base']
            fee = {'cost': feeCost, 'currency': feeCurrency}
        stopPrice = self.safe_string(order, 'stop-price')
        average = self.safe_string(order, 'trade_avg_price')
        trades = self.safe_value(order, 'trades')
        return self.safe_order({'info': order, 'id': id, 'clientOrderId': clientOrderId, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'lastTradeTimestamp': None, 'symbol': market['symbol'], 'type': type, 'timeInForce': None, 'postOnly': None, 'side': side, 'price': price, 'stopPrice': stopPrice, 'average': average, 'cost': cost, 'amount': amount, 'filled': filled, 'remaining': None, 'status': status, 'fee': fee, 'trades': trades}, market)

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        marketType, query = self.handle_market_type_and_params('createOrder', market, params)
        method = self.get_supported_mapping(marketType, {'spot': 'createSpotOrder', 'swap': 'createContractOrder', 'future': 'createContractOrder'})
        if method is None:
            raise NotSupported(self.id + ' createOrder() does not support ' + marketType + ' markets yet')
        return await getattr(self, method)(symbol, type, side, amount, price, query)

    async def create_spot_order(self, symbol, type, side, amount, price=None, params={}):
        await self.load_markets()
        await self.load_accounts()
        market = self.market(symbol)
        accountId = await self.fetch_account_id_by_type(market['type'])
        request = {'account-id': accountId, 'symbol': market['id']}
        orderType = type.replace('buy-', '')
        orderType = orderType.replace('sell-', '')
        options = self.safe_value(self.options, market['type'], {})
        stopPrice = self.safe_string_2(params, 'stopPrice', 'stop-price')
        if stopPrice is None:
            stopOrderTypes = self.safe_value(options, 'stopOrderTypes', {})
            if orderType in stopOrderTypes:
                raise ArgumentsRequired(self.id + ' createOrder() requires a stopPrice or a stop-price parameter for a stop order')
        else:
            stopOperator = self.safe_string(params, 'operator')
            if stopOperator is None:
                raise ArgumentsRequired(self.id + ' createOrder() requires an operator parameter "gte" or "lte" for a stop order')
            params = self.omit(params, ['stopPrice', 'stop-price'])
            request['stop-price'] = self.price_to_precision(symbol, stopPrice)
            request['operator'] = stopOperator
            if orderType == 'limit' or orderType == 'limit-fok':
                orderType = 'stop-' + orderType
            elif orderType != 'stop-limit' and orderType != 'stop-limit-fok':
                raise NotSupported(self.id + ' createOrder() does not support ' + type + ' orders')
        postOnly = self.safe_value(params, 'postOnly', False)
        if postOnly:
            orderType = 'limit-maker'
        request['type'] = side + '-' + orderType
        clientOrderId = self.safe_string_2(params, 'clientOrderId', 'client-order-id')
        if clientOrderId is None:
            broker = self.safe_value(self.options, 'broker', {})
            brokerId = self.safe_string(broker, 'id')
            request['client-order-id'] = brokerId + self.uuid()
        else:
            request['client-order-id'] = clientOrderId
        params = self.omit(params, ['clientOrderId', 'client-order-id', 'postOnly'])
        if orderType == 'market' and side == 'buy':
            if self.options['createMarketBuyOrderRequiresPrice']:
                if price is None:
                    raise InvalidOrder(self.id + " market buy order requires price argument to calculate cost(total amount of quote currency to spend for buying, amount * price). To switch off self warning exception and specify cost in the amount argument, set .options['createMarketBuyOrderRequiresPrice'] = False. Make sure you know what you're doing.")
                else:
                    request['amount'] = self.cost_to_precision(symbol, float(amount) * float(price))
            else:
                request['amount'] = self.cost_to_precision(symbol, amount)
        else:
            request['amount'] = self.amount_to_precision(symbol, amount)
        limitOrderTypes = self.safe_value(options, 'limitOrderTypes', {})
        if orderType in limitOrderTypes:
            request['price'] = self.price_to_precision(symbol, price)
        response = await self.spotPrivatePostV1OrderOrdersPlace(self.extend(request, params))
        id = self.safe_string(response, 'data')
        return {'info': response, 'id': id, 'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 'status': None, 'symbol': None, 'type': None, 'side': None, 'price': None, 'amount': None, 'filled': None, 'remaining': None, 'cost': None, 'trades': None, 'fee': None, 'clientOrderId': None, 'average': None}

    async def create_contract_order(self, symbol, type, side, amount, price=None, params={}):
        offset = self.safe_string(params, 'offset')
        if offset is None:
            raise ArgumentsRequired(self.id + ' createOrder() requires a string offset parameter for contract orders, open or close')
        stopPrice = self.safe_string(params, 'stopPrice')
        if stopPrice is not None:
            raise NotSupported(self.id + ' createOrder() supports tp_trigger_price + tp_order_price for take profit orders and/or sl_trigger_price + sl_order price for stop loss orders, stop orders are supported only with open long orders and open short orders')
        market = self.market(symbol)
        request = {'contract_code': market['id'], 'volume': self.amount_to_precision(symbol, amount), 'direction': side, 'offset': offset, 'lever_rate': 1}
        stopLossOrderPrice = self.safe_string(params, 'sl_order_price')
        stopLossTriggerPrice = self.safe_string(params, 'sl_trigger_price')
        takeProfitOrderPrice = self.safe_string(params, 'tp_order_price')
        takeProfitTriggerPrice = self.safe_string(params, 'tp_trigger_price')
        isOpenOrder = offset == 'open'
        isStopOrder = False
        if stopLossTriggerPrice is not None:
            request['sl_trigger_price'] = self.price_to_precision(symbol, stopLossTriggerPrice)
            isStopOrder = True
            if price is not None:
                request['sl_order_price'] = self.price_to_precision(symbol, price)
        if stopLossOrderPrice is not None:
            request['sl_order_price'] = self.price_to_precision(symbol, stopLossOrderPrice)
            isStopOrder = True
        if takeProfitTriggerPrice is not None:
            request['tp_trigger_price'] = self.price_to_precision(symbol, takeProfitTriggerPrice)
            isStopOrder = True
            if price is not None:
                request['tp_order_price'] = self.price_to_precision(symbol, price)
        if takeProfitOrderPrice is not None:
            request['tp_order_price'] = self.price_to_precision(symbol, takeProfitOrderPrice)
            isStopOrder = True
        if isStopOrder and (not isOpenOrder):
            raise NotSupported(self.id + ' createOrder() supports tp_trigger_price + tp_order_price for take profit orders and/or sl_trigger_price + sl_order price for stop loss orders, stop orders are supported only with open long orders and open short orders')
        params = self.omit(params, ['sl_order_price', 'sl_trigger_price', 'tp_order_price', 'tp_trigger_price'])
        postOnly = self.safe_value(params, 'postOnly', False)
        if postOnly:
            type = 'post_only'
        if type == 'limit' or type == 'ioc' or type == 'fok' or (type == 'post_only'):
            request['price'] = self.price_to_precision(symbol, price)
        request['order_price_type'] = type
        broker = self.safe_value(self.options, 'broker', {})
        brokerId = self.safe_string(broker, 'id')
        request['channel_code'] = brokerId
        clientOrderId = self.safe_string_2(params, 'client_order_id', 'clientOrderId')
        if clientOrderId is not None:
            request['client_order_id'] = clientOrderId
            params = self.omit(params, ['client_order_id', 'clientOrderId'])
        method = None
        if market['linear']:
            defaultMargin = 'cross' if market['future'] else 'isolated'
            marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
            if marginMode == 'isolated':
                method = 'contractPrivatePostLinearSwapApiV1SwapOrder'
            elif marginMode == 'cross':
                method = 'contractPrivatePostLinearSwapApiV1SwapCrossOrder'
        elif market['inverse']:
            if market['swap']:
                method = 'contractPrivatePostSwapApiV1SwapOrder'
            elif market['future']:
                method = 'contractPrivatePostApiV1ContractOrder'
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', {})
        return self.parse_order(data, market)

    async def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: unified symbol of the market the order was made in
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('cancelOrder', None, params)
        request = {}
        method = None
        market = None
        if marketType == 'spot':
            clientOrderId = self.safe_string_2(params, 'client-order-id', 'clientOrderId')
            method = 'spotPrivatePostV1OrderOrdersOrderIdSubmitcancel'
            if clientOrderId is None:
                request['order-id'] = id
            else:
                request['client-order-id'] = clientOrderId
                method = 'spotPrivatePostV1OrderOrdersSubmitCancelClientOrder'
                params = self.omit(params, ['client-order-id', 'clientOrderId'])
        else:
            if symbol is None:
                raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol for ' + marketType + ' orders')
            market = self.market(symbol)
            request['contract_code'] = market['id']
            if market['linear']:
                defaultMargin = 'cross' if market['future'] else 'isolated'
                marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
                if marginMode == 'isolated':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCancel'
                elif marginMode == 'cross':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCrossCancel'
            elif market['inverse']:
                if market['future']:
                    method = 'contractPrivatePostApiV1ContractCancel'
                    request['symbol'] = market['settleId']
                elif market['swap']:
                    method = 'contractPrivatePostSwapApiV1SwapCancel'
            else:
                raise NotSupported(self.id + ' cancelOrder() does not support ' + marketType + ' markets')
            clientOrderId = self.safe_string_2(params, 'client_order_id', 'clientOrderId')
            if clientOrderId is None:
                request['order_id'] = id
            else:
                request['client_order_id'] = clientOrderId
                params = self.omit(params, ['client_order_id', 'clientOrderId'])
        response = await getattr(self, method)(self.extend(request, params))
        return self.extend(self.parse_order(response, market), {'id': id, 'status': 'canceled'})

    async def cancel_orders(self, ids, symbol=None, params={}):
        """
        cancel multiple orders
        :param [str] ids: order ids
        :param str|None symbol: unified market symbol, default is None
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: an list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('cancelOrders', None, params)
        request = {}
        method = None
        if marketType == 'spot':
            clientOrderIds = self.safe_value_2(params, 'client-order-id', 'clientOrderId')
            clientOrderIds = self.safe_value_2(params, 'client-order-ids', 'clientOrderIds', clientOrderIds)
            if clientOrderIds is None:
                if isinstance(clientOrderIds, str):
                    request['order-ids'] = ids
                else:
                    request['order-ids'] = ','.join(ids)
            else:
                if isinstance(clientOrderIds, str):
                    request['client-order-ids'] = clientOrderIds
                else:
                    request['client-order-ids'] = ','.join(clientOrderIds)
                params = self.omit(params, ['client-order-id', 'client-order-ids', 'clientOrderId', 'clientOrderIds'])
            method = 'spotPrivatePostV1OrderOrdersBatchcancel'
        else:
            if symbol is None:
                raise ArgumentsRequired(self.id + ' cancelOrders() requires a symbol for ' + marketType + ' orders')
            market = self.market(symbol)
            request['contract_code'] = market['id']
            if market['linear']:
                defaultMargin = 'cross' if market['future'] else 'isolated'
                marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
                if marginMode == 'isolated':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCancel'
                elif marginMode == 'cross':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCrossCancel'
            elif market['inverse']:
                if market['future']:
                    method = 'contractPrivatePostApiV1ContractCancel'
                    request['symbol'] = market['settleId']
                elif market['swap']:
                    method = 'contractPrivatePostSwapApiV1SwapCancel'
                else:
                    raise NotSupported(self.id + ' cancelOrders() does not support ' + marketType + ' markets')
            clientOrderIds = self.safe_string_2(params, 'client_order_id', 'clientOrderId')
            clientOrderIds = self.safe_string_2(params, 'client_order_ids', 'clientOrderIds', clientOrderIds)
            if clientOrderIds is None:
                request['order_id'] = ','.join(ids)
            else:
                request['client_order_id'] = clientOrderIds
                params = self.omit(params, ['client_order_id', 'client_order_ids', 'clientOrderId', 'clientOrderIds'])
        response = await getattr(self, method)(self.extend(request, params))
        return response

    async def cancel_all_orders(self, symbol=None, params={}):
        """
        cancel all open orders
        :param str|None symbol: unified market symbol, only orders in the market of self symbol are cancelled when symbol is not None
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `order structures <https://docs.ccxt.com/en/latest/manual.html#order-structure>`
        """
        await self.load_markets()
        marketType = None
        marketType, params = self.handle_market_type_and_params('cancelAllOrders', None, params)
        request = {}
        market = None
        method = None
        if marketType == 'spot':
            if symbol is not None:
                market = self.market(symbol)
                request['symbol'] = market['id']
            method = 'spotPrivatePostV1OrderOrdersBatchCancelOpenOrders'
        else:
            if symbol is None:
                raise ArgumentsRequired(self.id + ' cancelAllOrders() requires a symbol for ' + marketType + ' orders')
            market = self.market(symbol)
            request['contract_code'] = market['id']
            if market['linear']:
                defaultMargin = 'cross' if market['future'] else 'isolated'
                marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
                if marginMode == 'isolated':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCancelallall'
                elif marginMode == 'cross':
                    method = 'contractPrivatePostLinearSwapApiV1SwapCrossCancelall'
            elif market['inverse']:
                if marketType == 'future':
                    method = 'contractPrivatePostApiV1ContractCancelall'
                    request['symbol'] = market['settleId']
                elif marketType == 'swap':
                    method = 'contractPrivatePostSwapApiV1SwapCancelall'
                else:
                    raise NotSupported(self.id + ' cancelAllOrders() does not support ' + marketType + ' markets')
        response = await getattr(self, method)(self.extend(request, params))
        return response

    def safe_network(self, networkId):
        lastCharacterIndex = len(networkId) - 1
        lastCharacter = networkId[lastCharacterIndex]
        if lastCharacter == '1':
            networkId = networkId[0:lastCharacterIndex]
        networksById = {}
        return self.safe_string(networksById, networkId, networkId)

    def parse_deposit_address(self, depositAddress, currency=None):
        address = self.safe_string(depositAddress, 'address')
        tag = self.safe_string(depositAddress, 'addressTag')
        currencyId = self.safe_string(depositAddress, 'currency')
        currency = self.safe_currency(currencyId, currency)
        code = self.safe_currency_code(currencyId, currency)
        networkId = self.safe_string(depositAddress, 'chain')
        networks = self.safe_value(currency, 'networks', {})
        networksById = self.index_by(networks, 'id')
        networkValue = self.safe_value(networksById, networkId, networkId)
        network = self.safe_string(networkValue, 'network')
        note = self.safe_string(depositAddress, 'note')
        self.check_address(address)
        return {'currency': code, 'address': address, 'tag': tag, 'network': network, 'note': note, 'info': depositAddress}

    async def fetch_deposit_addresses_by_network(self, code, params={}):
        """
        fetch a dictionary of addresses for a currency, indexed by network
        :param str code: unified currency code of the currency for the deposit address
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a dictionary of `address structures <https://docs.ccxt.com/en/latest/manual.html#address-structure>` indexed by the network
        """
        await self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        response = await self.spotPrivateGetV2AccountDepositAddress(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        parsed = self.parse_deposit_addresses(data, [code], False)
        return self.index_by(parsed, 'network')

    async def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/en/latest/manual.html#address-structure>`
        """
        rawNetwork = self.safe_string_upper(params, 'network')
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper(networks, rawNetwork, rawNetwork)
        params = self.omit(params, 'network')
        response = await self.fetch_deposit_addresses_by_network(code, params)
        result = None
        if network is None:
            result = self.safe_value(response, code)
            if result is None:
                alias = self.safe_string(networks, code, code)
                result = self.safe_value(response, alias)
                if result is None:
                    defaultNetwork = self.safe_string(self.options, 'defaultNetwork', 'ERC20')
                    result = self.safe_value(response, defaultNetwork)
                    if result is None:
                        values = list(response.values())
                        result = self.safe_value(values, 0)
                        if result is None:
                            raise InvalidAddress(self.id + ' fetchDepositAddress() cannot find deposit address for ' + code)
            return result
        result = self.safe_value(response, network)
        if result is None:
            raise InvalidAddress(self.id + ' fetchDepositAddress() cannot find ' + network + ' deposit address for ' + code)
        return result

    async def fetch_withdraw_addresses_by_network(self, code, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id']}
        response = await self.spotPrivateGetV2AccountWithdrawAddress(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        parsed = self.parse_deposit_addresses(data, [code], False)
        return self.index_by(parsed, 'network')

    async def fetch_withdraw_address(self, code, params={}):
        rawNetwork = self.safe_string_upper(params, 'network')
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper(networks, rawNetwork, rawNetwork)
        params = self.omit(params, 'network')
        response = await self.fetch_withdraw_addresses_by_network(code, params)
        result = None
        if network is None:
            result = self.safe_value(response, code)
            if result is None:
                alias = self.safe_string(networks, code, code)
                result = self.safe_value(response, alias)
                if result is None:
                    defaultNetwork = self.safe_string(self.options, 'defaultNetwork', 'ERC20')
                    result = self.safe_value(response, defaultNetwork)
                    if result is None:
                        values = list(response.values())
                        result = self.safe_value(values, 0)
                        if result is None:
                            raise InvalidAddress(self.id + ' fetchWithdrawAddress() cannot find withdraw address for ' + code)
            return result
        result = self.safe_value(response, network)
        if result is None:
            raise InvalidAddress(self.id + ' fetchWithdrawAddress() cannot find ' + network + ' withdraw address for ' + code)
        return result

    async def fetch_deposits(self, code=None, since=None, limit=None, params={}):
        """
        fetch all deposits made to an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch deposits for
        :param int|None limit: the maximum number of deposits structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        if limit is None or limit > 100:
            limit = 100
        await self.load_markets()
        currency = None
        if code is not None:
            currency = self.currency(code)
        request = {'type': 'deposit', 'from': 0}
        if currency is not None:
            request['currency'] = currency['id']
        if limit is not None:
            request['size'] = limit
        response = await self.spotPrivateGetV1QueryDepositWithdraw(self.extend(request, params))
        return self.parse_transactions(response['data'], currency, since, limit)

    async def fetch_withdrawals(self, code=None, since=None, limit=None, params={}):
        """
        fetch all withdrawals made from an account
        :param str|None code: unified currency code
        :param int|None since: the earliest time in ms to fetch withdrawals for
        :param int|None limit: the maximum number of withdrawals structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `transaction structures <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        if limit is None or limit > 100:
            limit = 100
        await self.load_markets()
        currency = None
        if code is not None:
            currency = self.currency(code)
        request = {'type': 'withdraw', 'from': 0}
        if currency is not None:
            request['currency'] = currency['id']
        if limit is not None:
            request['size'] = limit
        response = await self.spotPrivateGetV1QueryDepositWithdraw(self.extend(request, params))
        return self.parse_transactions(response['data'], currency, since, limit)

    def parse_transaction(self, transaction, currency=None):
        timestamp = self.safe_integer(transaction, 'created-at')
        updated = self.safe_integer(transaction, 'updated-at')
        code = self.safe_currency_code(self.safe_string(transaction, 'currency'))
        type = self.safe_string(transaction, 'type')
        if type == 'withdraw':
            type = 'withdrawal'
        status = self.parse_transaction_status(self.safe_string(transaction, 'state'))
        tag = self.safe_string(transaction, 'address-tag')
        feeCost = self.safe_number(transaction, 'fee')
        if feeCost is not None:
            feeCost = abs(feeCost)
        address = self.safe_string(transaction, 'address')
        network = self.safe_string_upper(transaction, 'chain')
        return {'info': transaction, 'id': self.safe_string_2(transaction, 'id', 'data'), 'txid': self.safe_string(transaction, 'tx-hash'), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'network': network, 'address': address, 'addressTo': None, 'addressFrom': None, 'tag': tag, 'tagTo': None, 'tagFrom': None, 'type': type, 'amount': self.safe_number(transaction, 'amount'), 'currency': code, 'status': status, 'updated': updated, 'fee': {'currency': code, 'cost': feeCost, 'rate': None}}

    def parse_transaction_status(self, status):
        statuses = {'unknown': 'failed', 'confirming': 'pending', 'confirmed': 'ok', 'safe': 'ok', 'orphan': 'failed', 'submitted': 'pending', 'canceled': 'canceled', 'reexamine': 'pending', 'reject': 'failed', 'pass': 'pending', 'wallet-reject': 'failed', 'confirm-error': 'failed', 'repealed': 'failed', 'wallet-transfer': 'pending', 'pre-transfer': 'pending'}
        return self.safe_string(statuses, status, status)

    async def withdraw(self, code, amount, address, tag=None, params={}):
        """
        make a withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str|None tag:
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `transaction structure <https://docs.ccxt.com/en/latest/manual.html#transaction-structure>`
        """
        tag, params = self.handle_withdraw_tag_and_params(tag, params)
        await self.load_markets()
        self.check_address(address)
        currency = self.currency(code)
        request = {'address': address, 'amount': amount, 'currency': currency['id'].lower()}
        if tag is not None:
            request['addr-tag'] = tag
        networks = self.safe_value(self.options, 'networks', {})
        network = self.safe_string_upper(params, 'network')
        network = self.safe_string_lower(networks, network, network)
        if network is not None:
            if network == 'erc20':
                request['chain'] = currency['id'] + network
            else:
                request['chain'] = network + currency['id']
            params = self.omit(params, 'network')
        response = await self.spotPrivatePostV1DwWithdrawApiCreate(self.extend(request, params))
        return self.parse_transaction(response, currency)

    def parse_transfer(self, transfer, currency=None):
        id = self.safe_string(transfer, 'data')
        code = self.safe_currency_code(None, currency)
        return {'info': transfer, 'id': id, 'timestamp': None, 'datetime': None, 'currency': code, 'amount': None, 'fromAccount': None, 'toAccount': None, 'status': None}

    async def transfer(self, code, amount, fromAccount, toAccount, params={}):
        """
        transfer currency internally between wallets on the same account
        :param str code: unified currency code
        :param float amount: amount to transfer
        :param str fromAccount: account to transfer from
        :param str toAccount: account to transfer to
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `transfer structure <https://docs.ccxt.com/en/latest/manual.html#transfer-structure>`
        """
        await self.load_markets()
        currency = self.currency(code)
        type = self.safe_string(params, 'type')
        if type is None:
            accountsByType = self.safe_value(self.options, 'accountsByType', {})
            fromAccount = fromAccount.lower()
            toAccount = toAccount.lower()
            fromId = self.safe_string(accountsByType, fromAccount, fromAccount)
            toId = self.safe_string(accountsByType, toAccount, toAccount)
            type = fromId + '-to-' + toId
        request = {'currency': currency['id'], 'amount': float(self.currency_to_precision(code, amount)), 'type': type}
        response = await self.spotPrivatePostFuturesTransfer(self.extend(request, params))
        transfer = self.parse_transfer(response, currency)
        return self.extend(transfer, {'amount': amount, 'currency': code, 'fromAccount': fromAccount, 'toAccount': toAccount})

    async def fetch_borrow_rates_per_symbol(self, params={}):
        """
        fetch borrow rates for currencies within individual markets
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a dictionary of `borrow rate structures <https://docs.ccxt.com/en/latest/manual.html#borrow-rate-structure>` indexed by market symbol
        """
        await self.load_markets()
        response = await self.spotPrivateGetV1MarginLoanInfo(params)
        timestamp = self.milliseconds()
        data = self.safe_value(response, 'data', [])
        rates = {'info': response}
        for i in range(0, len(data)):
            rate = data[i]
            currencies = self.safe_value(rate, 'currencies', [])
            symbolRates = {}
            for j in range(0, len(currencies)):
                currency = currencies[j]
                currencyId = self.safe_string(currency, 'currency')
                code = self.safe_currency_code(currencyId, 'currency')
                symbolRates[code] = {'currency': code, 'rate': self.safe_number(currency, 'actual-rate'), 'span': 86400000, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp)}
            market = self.markets_by_id[self.safe_string(rate, 'symbol')]
            symbol = market['symbol']
            rates[symbol] = symbolRates
        return rates

    async def fetch_borrow_rates(self, params={}):
        """
        fetch the borrow interest rates of all currencies
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a list of `borrow rate structures <https://docs.ccxt.com/en/latest/manual.html#borrow-rate-structure>`
        """
        await self.load_markets()
        response = await self.spotPrivateGetV1MarginLoanInfo(params)
        timestamp = self.milliseconds()
        data = self.safe_value(response, 'data', [])
        rates = {}
        for i in range(0, len(data)):
            market = data[i]
            currencies = self.safe_value(market, 'currencies', [])
            for j in range(0, len(currencies)):
                currency = currencies[j]
                currencyId = self.safe_string(currency, 'currency')
                code = self.safe_currency_code(currencyId, 'currency')
                rates[code] = {'currency': code, 'rate': self.safe_number(currency, 'actual-rate'), 'span': 86400000, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': None}
        return rates

    async def fetch_funding_rate_history(self, symbol=None, since=None, limit=None, params={}):
        """
        fetches historical funding rate prices
        :param str|None symbol: unified symbol of the market to fetch the funding rate history for
        :param int|None since: not used by huobi, but filtered internally by ccxt
        :param int|None limit: not used by huobi, but filtered internally by ccxt
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `funding rate structures <https://docs.ccxt.com/en/latest/manual.html?#funding-rate-history-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchFundingRateHistory() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        request = {'contract_code': market['id']}
        method = None
        if market['inverse']:
            method = 'contractPublicGetSwapApiV1SwapHistoricalFundingRate'
        elif market['linear']:
            method = 'contractPublicGetLinearSwapApiV1SwapHistoricalFundingRate'
        else:
            raise NotSupported(self.id + ' fetchFundingRateHistory() supports inverse and linear swaps only')
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data')
        result = self.safe_value(data, 'data', [])
        rates = []
        for i in range(0, len(result)):
            entry = result[i]
            marketId = self.safe_string(entry, 'contract_code')
            symbol = self.safe_symbol(marketId)
            timestamp = self.safe_integer(entry, 'funding_time')
            rates.append({'info': entry, 'symbol': symbol, 'fundingRate': self.safe_number(entry, 'funding_rate'), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp)})
        sorted = self.sort_by(rates, 'timestamp')
        return self.filter_by_symbol_since_limit(sorted, market['symbol'], since, limit)

    def parse_funding_rate(self, contract, market=None):
        nextFundingRate = self.safe_number(contract, 'estimated_rate')
        fundingTimestamp = self.safe_integer(contract, 'funding_time')
        nextFundingTimestamp = self.safe_integer(contract, 'next_funding_time')
        marketId = self.safe_string(contract, 'contract_code')
        symbol = self.safe_symbol(marketId, market)
        return {'info': contract, 'symbol': symbol, 'markPrice': None, 'indexPrice': None, 'interestRate': None, 'estimatedSettlePrice': None, 'timestamp': None, 'datetime': None, 'fundingRate': self.safe_number(contract, 'funding_rate'), 'fundingTimestamp': fundingTimestamp, 'fundingDatetime': self.iso8601(fundingTimestamp), 'nextFundingRate': nextFundingRate, 'nextFundingTimestamp': nextFundingTimestamp, 'nextFundingDatetime': self.iso8601(nextFundingTimestamp), 'previousFundingRate': None, 'previousFundingTimestamp': None, 'previousFundingDatetime': None}

    async def fetch_funding_rate(self, symbol, params={}):
        """
        fetch the current funding rate
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `funding rate structure <https://docs.ccxt.com/en/latest/manual.html#funding-rate-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        method = None
        if market['inverse']:
            method = 'contractPublicGetSwapApiV1SwapFundingRate'
        elif market['linear']:
            method = 'contractPublicGetLinearSwapApiV1SwapFundingRate'
        else:
            raise NotSupported(self.id + ' fetchFundingRate() supports inverse and linear swaps only')
        request = {'contract_code': market['id']}
        response = await getattr(self, method)(self.extend(request, params))
        result = self.safe_value(response, 'data', {})
        return self.parse_funding_rate(result, market)

    async def fetch_funding_rates(self, symbols=None, params={}):
        """
        fetch the funding rate for multiple markets
        :param [str]|None symbols: list of unified market symbols
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a dictionary of `funding rates structures <https://docs.ccxt.com/en/latest/manual.html#funding-rates-structure>`, indexe by market symbols
        """
        await self.load_markets()
        options = self.safe_value(self.options, 'fetchFundingRates', {})
        defaultSubType = self.safe_string(self.options, 'defaultSubType', 'inverse')
        subType = self.safe_string(options, 'subType', defaultSubType)
        subType = self.safe_string(params, 'subType', subType)
        request = {}
        method = self.get_supported_mapping(subType, {'linear': 'contractPublicGetLinearSwapApiV1SwapBatchFundingRate', 'inverse': 'contractPublicGetSwapApiV1SwapBatchFundingRate'})
        params = self.omit(params, 'subType')
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        result = self.parse_funding_rates(data)
        return self.filter_by_array(result, 'symbol', symbols)

    async def fetch_borrow_interest(self, code=None, symbol=None, since=None, limit=None, params={}):
        """
        fetch the interest owed by the user for borrowing currency for margin trading
        :param str|None code: unified currency code
        :param str|None symbol: unified market symbol when fetch interest in isolated markets
        :param int|None since: the earliest time in ms to fetch borrrow interest for
        :param int|None limit: the maximum number of structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `borrow interest structures <https://docs.ccxt.com/en/latest/manual.html#borrow-interest-structure>`
        """
        await self.load_markets()
        defaultMargin = self.safe_string(params, 'marginMode', 'cross')
        marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
        request = {}
        if since is not None:
            request['start-date'] = self.yyyymmdd(since)
        if limit is not None:
            request['size'] = limit
        market = None
        method = None
        if marginMode == 'isolated':
            method = 'privateGetMarginLoanOrders'
            if symbol is not None:
                market = self.market(symbol)
                request['symbol'] = market['id']
        else:
            method = 'privateGetCrossMarginLoanOrders'
            if code is not None:
                currency = self.currency(code)
                request['currency'] = currency['id']
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data')
        interest = self.parse_borrow_interests(data, market)
        return self.filter_by_currency_since_limit(interest, code, since, limit)

    def parse_borrow_interest(self, info, market=None):
        marketId = self.safe_string(info, 'symbol')
        marginMode = 'cross' if marketId is None else 'isolated'
        market = self.safe_market(marketId)
        symbol = self.safe_string(market, 'symbol')
        timestamp = self.safe_number(info, 'accrued-at')
        return {'account': symbol if marginMode == 'isolated' else 'cross', 'symbol': symbol, 'marginMode': marginMode, 'currency': self.safe_currency_code(self.safe_string(info, 'currency')), 'interest': self.safe_number(info, 'interest-amount'), 'interestRate': self.safe_number(info, 'interest-rate'), 'amountBorrowed': self.safe_number(info, 'loan-amount'), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': info}

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = '/'
        query = self.omit(params, self.extract_params(path))
        if isinstance(api, str):
            if api == 'market':
                url += api
            elif api == 'public' or api == 'private':
                url += self.version
            elif api == 'v2Public' or api == 'v2Private':
                url += 'v2'
            url += '/' + self.implode_params(path, params)
            if api == 'private' or api == 'v2Private':
                self.check_required_credentials()
                timestamp = self.ymdhms(self.milliseconds(), 'T')
                request = {'SignatureMethod': 'HmacSHA256', 'SignatureVersion': '2', 'AccessKeyId': self.apiKey, 'Timestamp': timestamp}
                if method != 'POST':
                    request = self.extend(request, query)
                request = self.keysort(request)
                auth = self.urlencode(request)
                payload = '\n'.join([method, self.hostname, url, auth])
                signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
                auth += '&' + self.urlencode({'Signature': signature})
                url += '?' + auth
                if method == 'POST':
                    body = self.json(query)
                    headers = {'Content-Type': 'application/json'}
                else:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            elif query:
                url += '?' + self.urlencode(query)
            url = self.implode_params(self.urls['api'][api], {'hostname': self.hostname}) + url
        else:
            type = self.safe_string(api, 0)
            access = self.safe_string(api, 1)
            levelOneNestedPath = self.safe_string(api, 2)
            levelTwoNestedPath = self.safe_string(api, 3)
            hostname = None
            hostnames = self.safe_value(self.urls['hostnames'], type)
            if not isinstance(hostnames, str):
                hostnames = self.safe_value(hostnames, levelOneNestedPath)
                if not isinstance(hostname, str) and levelTwoNestedPath is not None:
                    hostnames = self.safe_value(hostnames, levelTwoNestedPath)
            hostname = hostnames
            url += self.implode_params(path, params)
            if access == 'public':
                if query:
                    url += '?' + self.urlencode(query)
            elif access == 'private':
                self.check_required_credentials()
                timestamp = self.ymdhms(self.milliseconds(), 'T')
                request = {'SignatureMethod': 'HmacSHA256', 'SignatureVersion': '2', 'AccessKeyId': self.apiKey, 'Timestamp': timestamp}
                if method != 'POST':
                    request = self.extend(request, query)
                request = self.keysort(request)
                auth = self.urlencode(request)
                payload = '\n'.join([method, hostname, url, auth])
                signature = self.hmac(self.encode(payload), self.encode(self.secret), hashlib.sha256, 'base64')
                auth += '&' + self.urlencode({'Signature': signature})
                url += '?' + auth
                if method == 'POST':
                    body = self.json(query)
                    headers = {'Content-Type': 'application/json'}
                else:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            url = self.implode_params(self.urls['api'][type], {'hostname': hostname}) + url
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def calculate_rate_limiter_cost(self, api, method, path, params, config={}, context={}):
        return self.safe_integer(config, 'cost', 1)

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        if 'status' in response:
            status = self.safe_string(response, 'status')
            if status == 'error':
                code = self.safe_string_2(response, 'err-code', 'err_code')
                feedback = self.id + ' ' + body
                self.throw_broadly_matched_exception(self.exceptions['broad'], body, feedback)
                self.throw_exactly_matched_exception(self.exceptions['exact'], code, feedback)
                message = self.safe_string_2(response, 'err-msg', 'err_msg')
                self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
                raise ExchangeError(feedback)

    async def fetch_funding_history(self, symbol=None, since=None, limit=None, params={}):
        """
        fetch the history of funding payments paid and received on self account
        :param str|None symbol: unified market symbol
        :param int|None since: the earliest time in ms to fetch funding history for
        :param int|None limit: the maximum number of funding history structures to retrieve
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `funding history structure <https://docs.ccxt.com/en/latest/manual.html#funding-history-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        marketType, query = self.handle_market_type_and_params('fetchFundingHistory', market, params)
        method = None
        request = {'type': '30,31'}
        if market['linear']:
            method = 'contractPrivatePostLinearSwapApiV1SwapFinancialRecordExact'
            defaultMargin = 'cross' if market['future'] else 'isolated'
            marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
            if marginMode == 'isolated':
                request['margin_account'] = market['id']
            else:
                request['margin_account'] = market['quoteId']
        elif marketType == 'swap':
            method = 'contractPrivatePostSwapApiV1SwapFinancialRecordExact'
            request['contract_code'] = market['id']
        else:
            raise ExchangeError(self.id + ' fetchFundingHistory() only makes sense for swap contracts')
        response = await getattr(self, method)(self.extend(request, query))
        data = self.safe_value(response, 'data', {})
        financialRecord = self.safe_value(data, 'financial_record', [])
        return self.parse_incomes(financialRecord, market, since, limit)

    async def set_leverage(self, leverage, symbol=None, params={}):
        """
        set the level of leverage for a market
        :param float leverage: the rate of leverage
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: response from the exchange
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' setLeverage() requires a symbol argument')
        await self.load_markets()
        market = self.market(symbol)
        marketType, query = self.handle_market_type_and_params('setLeverage', market, params)
        method = None
        if market['linear']:
            defaultMargin = 'cross' if market['future'] else 'isolated'
            marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', defaultMargin)
            method = self.get_supported_mapping(marginMode, {'isolated': 'contractPrivatePostLinearSwapApiV1SwapSwitchLeverRate', 'cross': 'contractPrivatePostLinearSwapApiV1SwapCrossSwitchLeverRate'})
        else:
            method = self.get_supported_mapping(marketType, {'future': 'contractPrivatePostApiV1ContractSwitchLeverRate', 'swap': 'contractPrivatePostSwapApiV1SwapSwitchLeverRate'})
        request = {'lever_rate': leverage}
        if marketType == 'future' and market['inverse']:
            request['symbol'] = market['settleId']
        else:
            request['contract_code'] = market['id']
        response = await getattr(self, method)(self.extend(request, query))
        return response

    def parse_income(self, income, market=None):
        marketId = self.safe_string(income, 'contract_code')
        symbol = self.safe_symbol(marketId, market)
        amount = self.safe_number(income, 'amount')
        timestamp = self.safe_integer(income, 'ts')
        id = self.safe_string(income, 'id')
        currencyId = self.safe_string_2(income, 'symbol', 'asset')
        code = self.safe_currency_code(currencyId)
        return {'info': income, 'symbol': symbol, 'code': code, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'id': id, 'amount': amount}

    def parse_incomes(self, incomes, market=None, since=None, limit=None):
        result = []
        for i in range(0, len(incomes)):
            entry = incomes[i]
            parsed = self.parse_income(entry, market)
            result.append(parsed)
        sorted = self.sort_by(result, 'timestamp')
        return self.filter_by_since_limit(sorted, since, limit, 'timestamp')

    def parse_position(self, position, market=None):
        market = self.safe_market(self.safe_string(position, 'contract_code'))
        symbol = market['symbol']
        contracts = self.safe_string(position, 'volume')
        contractSize = self.safe_value(market, 'contractSize')
        contractSizeString = self.number_to_string(contractSize)
        entryPrice = self.safe_number(position, 'cost_open')
        initialMargin = self.safe_string(position, 'position_margin')
        rawSide = self.safe_string(position, 'direction')
        side = 'long' if rawSide == 'buy' else 'short'
        unrealizedProfit = self.safe_number(position, 'profit_unreal')
        marginMode = self.safe_string(position, 'margin_mode')
        leverage = self.safe_string(position, 'lever_rate')
        percentage = Precise.string_mul(self.safe_string(position, 'profit_rate'), '100')
        lastPrice = self.safe_string(position, 'last_price')
        faceValue = Precise.string_mul(contracts, contractSizeString)
        notional = None
        if market['linear']:
            notional = Precise.string_mul(faceValue, lastPrice)
        else:
            notional = Precise.string_div(faceValue, lastPrice)
            marginMode = 'cross'
        intialMarginPercentage = Precise.string_div(initialMargin, notional)
        collateral = self.safe_string(position, 'margin_balance')
        liquidationPrice = self.safe_number(position, 'liquidation_price')
        adjustmentFactor = self.safe_string(position, 'adjust_factor')
        maintenanceMarginPercentage = Precise.string_div(adjustmentFactor, leverage)
        maintenanceMargin = Precise.string_mul(maintenanceMarginPercentage, notional)
        marginRatio = Precise.string_div(maintenanceMargin, collateral)
        return {'info': position, 'symbol': symbol, 'contracts': self.parse_number(contracts), 'contractSize': contractSize, 'entryPrice': entryPrice, 'collateral': self.parse_number(collateral), 'side': side, 'unrealizedProfit': unrealizedProfit, 'leverage': self.parse_number(leverage), 'percentage': self.parse_number(percentage), 'marginMode': marginMode, 'notional': self.parse_number(notional), 'markPrice': None, 'liquidationPrice': liquidationPrice, 'initialMargin': self.parse_number(initialMargin), 'initialMarginPercentage': self.parse_number(intialMarginPercentage), 'maintenanceMargin': self.parse_number(maintenanceMargin), 'maintenanceMarginPercentage': self.parse_number(maintenanceMarginPercentage), 'marginRatio': self.parse_number(marginRatio), 'timestamp': None, 'datetime': None}

    async def fetch_positions(self, symbols=None, params={}):
        """
        fetch all open positions
        :param [str]|None symbols: list of unified market symbols
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns [dict]: a list of `position structure <https://docs.ccxt.com/en/latest/manual.html#position-structure>`
        """
        await self.load_markets()
        marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', 'isolated')
        defaultSubType = self.safe_string(self.options, 'defaultSubType', 'inverse')
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchPositions', None, params)
        if marketType == 'spot':
            marketType = 'future'
        method = None
        if defaultSubType == 'linear':
            method = self.get_supported_mapping(marginMode, {'isolated': 'contractPrivatePostLinearSwapApiV1SwapPositionInfo', 'cross': 'contractPrivatePostLinearSwapApiV1SwapCrossPositionInfo'})
        else:
            method = self.get_supported_mapping(marketType, {'future': 'contractPrivatePostApiV1ContractPositionInfo', 'swap': 'contractPrivatePostSwapApiV1SwapPositionInfo'})
        response = await getattr(self, method)(params)
        data = self.safe_value(response, 'data', [])
        timestamp = self.safe_integer(response, 'ts')
        result = []
        for i in range(0, len(data)):
            position = data[i]
            parsed = self.parse_position(position)
            result.append(self.extend(parsed, {'timestamp': timestamp, 'datetime': self.iso8601(timestamp)}))
        return self.filter_by_array(result, 'symbol', symbols, False)

    async def fetch_position(self, symbol, params={}):
        """
        fetch data on a single open contract trade position
        :param str symbol: unified market symbol of the market the position is held in, default is None
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `position structure <https://docs.ccxt.com/en/latest/manual.html#position-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        marginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', 'isolated')
        marginMode = self.safe_string_2(params, 'marginMode', 'defaultMarginMode', marginMode)
        params = self.omit(params, ['defaultMarginMode', 'marginMode'])
        marketType, query = self.handle_market_type_and_params('fetchPosition', market, params)
        method = None
        if market['linear']:
            method = self.get_supported_mapping(marginMode, {'isolated': 'contractPrivatePostLinearSwapApiV1SwapAccountPositionInfo', 'cross': 'contractPrivatePostLinearSwapApiV1SwapCrossAccountPositionInfo'})
        else:
            method = self.get_supported_mapping(marketType, {'future': 'contractPrivatePostApiV1ContractAccountPositionInfo', 'swap': 'contractPrivatePostSwapApiV1SwapAccountPositionInfo'})
        request = {}
        if market['future'] and market['inverse']:
            request['symbol'] = market['settleId']
        else:
            if marginMode == 'cross':
                request['margin_account'] = 'USDT'
            request['contract_code'] = market['id']
        response = await getattr(self, method)(self.extend(request, query))
        data = self.safe_value(response, 'data')
        account = None
        if marginMode == 'cross':
            account = data
        else:
            account = self.safe_value(data, 0)
        omitted = self.omit(account, ['positions'])
        positions = self.safe_value(account, 'positions')
        position = None
        if market['future'] and market['inverse']:
            for i in range(0, len(positions)):
                entry = positions[i]
                if entry['contract_code'] == market['id']:
                    position = entry
                    break
        else:
            position = self.safe_value(positions, 0)
        timestamp = self.safe_integer(response, 'ts')
        parsed = self.parse_position(self.extend(position, omitted))
        return self.extend(parsed, {'timestamp': timestamp, 'datetime': self.iso8601(timestamp)})

    def parse_ledger_entry_type(self, type):
        types = {'trade': 'trade', 'etf': 'trade', 'transact-fee': 'fee', 'fee-deduction': 'fee', 'transfer': 'transfer', 'credit': 'credit', 'liquidation': 'trade', 'interest': 'credit', 'deposit': 'deposit', 'withdraw': 'withdrawal', 'withdraw-fee': 'fee', 'exchange': 'exchange', 'other-types': 'transfer', 'rebate': 'rebate'}
        return self.safe_string(types, type, type)

    def parse_ledger_entry(self, item, currency=None):
        id = self.safe_string(item, 'transactId')
        currencyId = self.safe_string(item, 'currency')
        code = self.safe_currency_code(currencyId, currency)
        amount = self.safe_number(item, 'transactAmt')
        transferType = self.safe_string(item, 'transferType')
        type = self.parse_ledger_entry_type(transferType)
        direction = self.safe_string(item, 'direction')
        timestamp = self.safe_integer(item, 'transactTime')
        datetime = self.iso8601(timestamp)
        account = self.safe_string(item, 'accountId')
        return {'id': id, 'direction': direction, 'account': account, 'referenceId': id, 'referenceAccount': account, 'type': type, 'currency': code, 'amount': amount, 'timestamp': timestamp, 'datetime': datetime, 'before': None, 'after': None, 'status': None, 'fee': None, 'info': item}

    async def fetch_ledger(self, code=None, since=None, limit=None, params={}):
        """
        fetch the history of changes, actions done by the user or operations that altered balance of the user
        :param str|None code: unified currency code, default is None
        :param int|None since: timestamp in ms of the earliest ledger entry, default is None
        :param int|None limit: max number of ledger entrys to return, default is None
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `ledger structure <https://docs.ccxt.com/en/latest/manual.html#ledger-structure>`
        """
        await self.load_markets()
        accountId = await self.fetch_account_id_by_type('spot', params)
        request = {'accountId': accountId}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['currency'] = currency['id']
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = await self.spotPrivateGetV2AccountLedger(self.extend(request, params))
        data = self.safe_value(response, 'data', [])
        return self.parse_ledger(data, currency, since, limit)

    async def fetch_leverage_tiers(self, symbols=None, params={}):
        """
        retrieve information on the maximum leverage, and maintenance margin for trades of varying trade sizes
        :param [str]|None symbols: list of unified market symbols
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a dictionary of `leverage tiers structures <https://docs.ccxt.com/en/latest/manual.html#leverage-tiers-structure>`, indexed by market symbols
        """
        await self.load_markets()
        response = await self.contractPublicGetLinearSwapApiV1SwapAdjustfactor(params)
        data = self.safe_value(response, 'data')
        return self.parse_leverage_tiers(data, symbols, 'contract_code')

    async def fetch_market_leverage_tiers(self, symbol, params={}):
        """
        retrieve information on the maximum leverage, and maintenance margin for trades of varying trade sizes for a single market
        :param str symbol: unified market symbol
        :param dict params: extra parameters specific to the huobi api endpoint
        :returns dict: a `leverage tiers structure <https://docs.ccxt.com/en/latest/manual.html#leverage-tiers-structure>`
        """
        await self.load_markets()
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            if not market['contract']:
                raise BadRequest(self.id + ' fetchMarketLeverageTiers() symbol supports contract markets only')
            request['contract_code'] = market['id']
        response = await self.contractPublicGetLinearSwapApiV1SwapAdjustfactor(self.extend(request, params))
        data = self.safe_value(response, 'data')
        tiers = self.parse_leverage_tiers(data, [symbol], 'contract_code')
        return self.safe_value(tiers, symbol)

    def parse_leverage_tiers(self, response, symbols=None, marketIdKey=None):
        result = {}
        for i in range(0, len(response)):
            item = response[i]
            list = self.safe_value(item, 'list', [])
            tiers = []
            currency = self.safe_string(item, 'trade_partition')
            id = self.safe_string(item, marketIdKey)
            symbol = self.safe_symbol(id)
            if self.in_array(symbols, symbol):
                for j in range(0, len(list)):
                    obj = list[j]
                    leverage = self.safe_string(obj, 'lever_rate')
                    ladders = self.safe_value(obj, 'ladders', [])
                    for k in range(0, len(ladders)):
                        bracket = ladders[k]
                        adjustFactor = self.safe_string(bracket, 'adjust_factor')
                        tiers.append({'tier': self.safe_integer(bracket, 'ladder'), 'currency': self.safe_currency_code(currency), 'minNotional': self.safe_number(bracket, 'min_size'), 'maxNotional': self.safe_number(bracket, 'max_size'), 'maintenanceMarginRate': self.parse_number(Precise.string_div(adjustFactor, leverage)), 'maxLeverage': self.parse_number(leverage), 'info': bracket})
                result[symbol] = tiers
        return result

    async def fetch_open_interest_history(self, symbol, timeframe='1h', since=None, limit=None, params={}):
        """
        Retrieves the open intestest history of a currency
        :param str symbol: Unified CCXT market symbol
        :param str timeframe: '1h', '4h', '12h', or '1d'
        :param int|None since: Not used by huobi api, but response parsed by CCXT
        :param int|None limit: Default：48，Data Range [1,200]
        :param dict params: Exchange specific parameters
        :param int params['amount_type']: *required* Open interest unit. 1-cont，2-cryptocurrenty
        :param int|None params['pair']: eg BTC-USDT *Only for USDT-M*
        :returns dict: an array of `open interest structures <https://docs.ccxt.com/en/latest/manual.html#open-interest-structure>`
        """
        if timeframe != '1h' and timeframe != '4h' and (timeframe != '12h') and (timeframe != '1d'):
            raise BadRequest(self.id + ' fetchOpenInterestHistory cannot only use the 1h, 4h, 12h and 1d timeframe')
        await self.load_markets()
        timeframes = {'1h': '60min', '4h': '4hour', '12h': '12hour', '1d': '1day'}
        market = self.market(symbol)
        amountType = self.safe_number_2(params, 'amount_type', 'amountType')
        if amountType is None:
            raise ArgumentsRequired(self.id + ' fetchOpenInterestHistory requires parameter params.amountType to be either 1(cont), or 2(cryptocurrenty)')
        request = {'period': timeframes[timeframe], 'amount_type': amountType}
        method = None
        if market['future']:
            request['contract_type'] = self.safe_string(market['info'], 'contract_type')
            request['symbol'] = market['baseId']
            method = 'contractPublicGetApiV1ContractHisOpenInterest'
        elif market['linear']:
            request['contract_type'] = 'swap'
            request['contract_code'] = market['id']
            request['contract_code'] = market['id']
            method = 'contractPublicGetLinearSwapApiV1SwapHisOpenInterest'
        else:
            request['contract_code'] = market['id']
            method = 'contractPublicGetSwapApiV1SwapHisOpenInterest'
        if limit is not None:
            request['size'] = limit
        response = await getattr(self, method)(self.extend(request, params))
        data = self.safe_value(response, 'data')
        tick = self.safe_value(data, 'tick')
        return self.parse_open_interests(tick, None, since, limit)

    def parse_open_interest(self, interest, market=None):
        timestamp = self.safe_number(interest, 'ts')
        return {'symbol': self.safe_string(market, 'symbol'), 'baseVolume': self.safe_number(interest, 'volume'), 'quoteVolume': self.safe_value(interest, 'value'), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': interest}

    async def borrow_margin(self, code, amount, symbol=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        request = {'currency': currency['id'], 'amount': self.currency_to_precision(code, amount)}
        defaultMarginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', 'cross')
        marginMode = self.safe_string(params, 'marginMode', defaultMarginMode)
        method = None
        if marginMode == 'isolated':
            if symbol is None:
                raise ArgumentsRequired(self.id + ' borrowMargin() requires a symbol argument for isolated margin')
            market = self.market(symbol)
            request['symbol'] = market['id']
            method = 'privatePostMarginOrders'
        elif marginMode == 'cross':
            method = 'privatePostCrossMarginOrders'
        params = self.omit(params, 'marginMode')
        response = await getattr(self, method)(self.extend(request, params))
        transaction = self.parse_margin_loan(response, currency)
        return self.extend(transaction, {'amount': amount, 'symbol': symbol})

    async def repay_margin(self, code, amount, symbol=None, params={}):
        await self.load_markets()
        currency = self.currency(code)
        defaultMarginMode = self.safe_string_2(self.options, 'defaultMarginMode', 'marginMode', 'cross')
        marginMode = self.safe_string(params, 'marginMode', defaultMarginMode)
        params = self.omit(params, 'marginMode')
        marginAccounts = self.safe_value(self.options, 'marginAccounts', {})
        accountType = self.get_supported_mapping(marginMode, marginAccounts)
        accountId = await self.fetch_account_id_by_type(accountType, params)
        request = {'currency': currency['id'], 'amount': self.currency_to_precision(code, amount), 'accountId': accountId}
        response = await self.v2PrivatePostAccountRepayment(self.extend(request, params))
        data = self.safe_value(response, 'Data', [])
        loan = self.safe_value(data, 0)
        transaction = self.parse_margin_loan(loan, currency)
        return self.extend(transaction, {'amount': amount, 'symbol': symbol})

    def parse_margin_loan(self, info, currency=None):
        timestamp = self.safe_integer(info, 'repayTime')
        return {'id': self.safe_integer_2(info, 'repayId', 'data'), 'currency': self.safe_currency_code(None, currency), 'amount': None, 'symbol': None, 'timestamp': timestamp, 'datetime': self.iso8601(timestamp), 'info': info}

    async def fetch_settlement_history(self, symbol=None, since=None, limit=None, params={}):
        """
        Fetches historical settlement records
        :param str symbol: unified symbol of the market to fetch the settlement history for
        :param int since: timestamp in ms, value range = current time - 90 days，default = current time - 90 days
        :param int limit: page items, default 20, shall not exceed 50
        :param dict params: exchange specific params
        :param int params['until']: timestamp in ms, value range = start_time -> current time，default = current time
        :param int params['page_index']: page index, default page 1 if not filled
        :param int params['code']: unified currency code, can be used when symbol is None
        :returns: A list of settlement history objects
        """
        code = self.safe_string(params, 'code')
        until = self.safe_integer_2(params, 'until', 'till')
        params = self.omit(params, ['until', 'till'])
        market = None if symbol is None else self.market(symbol)
        type, query = self.handle_market_type_and_params('fetchSettlementHistory', market, params)
        if type == 'future':
            if symbol is None and code is None:
                raise ArgumentsRequired(self.id + ' requires a symbol argument or params["code"] for fetchSettlementHistory future')
        elif symbol is None:
            raise ArgumentsRequired(self.id + ' requires a symbol argument for fetchSettlementHistory swap')
        request = {}
        if market['future']:
            request['symbol'] = market['baseId']
        else:
            request['contract_code'] = market['id']
        if since is not None:
            request['start_at'] = since
        if limit is not None:
            request['page_size'] = limit
        if until is not None:
            request['end_at'] = until
        method = 'contractPublicGetApiV1ContractSettlementRecords'
        if market['swap']:
            if market['linear']:
                method = 'contractPublicGetLinearSwapApiV1SwapSettlementRecords'
            else:
                method = 'contractPublicGetSwapApiV1SwapSettlementRecords'
        response = await getattr(self, method)(self.extend(request, query))
        data = self.safe_value(response, 'data')
        settlementRecord = self.safe_value(data, 'settlement_record')
        settlements = self.parse_settlements(settlementRecord, market)
        return self.sort_by(settlements, 'timestamp')

    def parse_settlements(self, settlements, market):
        result = []
        for i in range(0, len(settlements)):
            settlement = settlements[i]
            list = self.safe_value(settlement, 'list')
            if list is not None:
                timestamp = self.safe_integer(settlement, 'settlement_time')
                timestampDetails = {'timestamp': timestamp, 'datetime': self.iso8601(timestamp)}
                for j in range(0, len(list)):
                    item = list[j]
                    parsedSettlement = self.parse_settlement(item, market)
                    result.append(self.extend(parsedSettlement, timestampDetails))
            else:
                result.append(self.parse_settlement(settlements[i], market))
        return result

    def parse_settlement(self, settlement, market):
        timestamp = self.safe_integer(settlement, 'settlement_time')
        marketId = self.safe_string(settlement, 'contract_code')
        return {'info': settlement, 'symbol': self.safe_symbol(marketId, market), 'price': self.safe_number(settlement, 'settlement_price'), 'timestamp': timestamp, 'datetime': self.iso8601(timestamp)}