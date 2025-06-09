import logging
from abc import ABCMeta, abstractmethod
from typing import Dict
from eth_utils import to_checksum_address
from blockapi.v2.base import BlockchainApi, IBalance
from blockapi.v2.models import BalanceItem, Coin, CoinInfo
logger = logging.getLogger(__name__)

class CovalentApiBase(BlockchainApi, IBalance, metaclass=ABCMeta):
    """
    API docs: https://www.covalenthq.com/docs/api/
    """
    API_BASE_URL = 'https://api.covalenthq.com/v1'
    API_BASE_RATE_LIMIT = 0.2

    @property
    @abstractmethod
    def api_options(self):
        pass

    @property
    @abstractmethod
    def CHAIN_ID(self):
        pass

    @property
    @abstractmethod
    def coin(self):
        pass
    supported_requests = {'get_balance': '/v1/{chain_id}/address/{address}/balances_v2/'}

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self._session.auth = (api_key, '')

    def get_balance(self, address: str) -> [BalanceItem]:
        response = self.get('get_balance', chain_id=self.CHAIN_ID, address=address)
        return self._parse_items(response)

    @staticmethod
    def to_checksum_address(address: str):
        try:
            return to_checksum_address(address)
        except ValueError as e:
            logger.exception(e)
            return address

    def _parse_items(self, response: Dict) -> [BalanceItem]:
        try:
            raw_balances = response['data']['items']
        except KeyError as e:
            logger.exception(e)
            return []
        balances = []
        for raw_balance in raw_balances:
            if raw_balance.get('balance') is None or raw_balance['balance'] == 0:
                logger.debug("Skipping coin: '%s' - balance is zero.", raw_balance.get('contract_name'))
                continue
            coin_symbol = raw_balance.get('contract_ticker_symbol')
            if coin_symbol == self.coin.symbol:
                coin = self.coin
            else:
                coin = Coin.from_api(symbol=raw_balance.get('contract_ticker_symbol'), name=raw_balance.get('contract_name'), decimals=raw_balance.get('contract_decimals', 0), blockchain=self.api_options.blockchain, address=self.to_checksum_address(raw_balance.get('contract_address')), standards=raw_balance.get('supports_erc', []), info=CoinInfo(logo_url=raw_balance.get('logo_url')))
            balances.append(BalanceItem.from_api(balance_raw=raw_balance.get('balance'), coin=coin, last_updated=raw_balance.get('last_transferred_at'), raw=raw_balance))
        return balances