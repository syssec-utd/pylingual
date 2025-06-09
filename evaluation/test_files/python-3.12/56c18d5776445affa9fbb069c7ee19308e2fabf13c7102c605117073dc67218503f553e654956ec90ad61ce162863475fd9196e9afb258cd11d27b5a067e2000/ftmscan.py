import os
import time
import logging
import pandas as pd
import requests
from typing import Any, Dict, List, TypedDict, Union

class FTMScanConnector:
    api_endpoint_preamble: str = 'https://api.ftmscan.com/api?'
    API_KEY: str = os.environ['FTMSCAN_API_KEY']

    def __init__(self, max_api_calls_sec: int=5):
        self._api_call_sleep_time = 1 / max_api_calls_sec

    def _rate_limit(self) -> None:
        time.sleep(self._api_call_sleep_time)

    @staticmethod
    def _validate_timestamp_format(self, timestamp: Union[int, str, pd.Timestamp]):
        raise NotImplementedError()

    def run_query(self, query: str, rate_limit: bool=True) -> Dict[str, Any]:
        """Func is wrapped with some ultimate limiters to ensure this method is 
        never callled too much.  However, the batch-call function should also 
        limit itself, since it is likely to have a higher-level awareness (at 
        least passed in by the caller) as to how the rate itself should be 
        spread across different token-pairs

        Args: 
            query (str): URL/API endpoint to query with Requests.request.get()

        Returns:
            (dict): Component of the requests.Response object
        """
        headers = {'Content-Type': 'application/json'}
        try:
            response: requests.Response = requests.get(query, headers=headers)
            if not (response and response.ok):
                msg = f'Failed request with status code {response.status_code}' + f': {response.text}'
                logging.warning(msg)
                raise Exception(msg)
            if rate_limit:
                self._rate_limit()
            return response.json()['result']
        except Exception:
            logging.exception(f'Problem in query: {query}')
            raise

    def account_balance_single_address(self, address: str) -> float:
        """Get FTM Balance for a single address."""
        query_url: str = ''.join([self.api_endpoint_preamble, 'module=account&action=balance', f'&address={address}', '&tag=latest', f'&apikey={self.API_KEY}'])
        balance: str = self.run_query(query=query_url)
        return float(balance)

    def tx_receipt_list(self, address: str, startblock: int=0, endblock: int=99999999) -> List['TxReceipt']:
        query_url: str = ''.join([self.api_endpoint_preamble, 'module=account', f'&action=txlist&address={address}', f'&startblock={startblock}', f'&endblock={endblock}', '&sort=asc', f'&apikey={self.API_KEY}'])
        tx_receipts = self.run_query(query=query_url)
        return tx_receipts

class TxReceipt(TypedDict):
    """An Ethereum (Fantom) transaction receipt from the Etherscan (FTMScan) API.

    Keys (value_type): 
        gasPrice (int): Gas price at the time of the transaction. 
            A base 16 encoded integer units of Wei.
        gasUsed (int): Gas usage by the transaction. A base 16 encoded integer
            in units of Wei. Thus, `int(gasUsed, base=16)` is an integer.  
        cumulativeGasUsed: int
        from: Address the transaction was sent from.
        to: 
        blockHash: Any
        blockNumber: Any
        contractAddress: Any
        logs: dict
        logsBloom: Any
        status: Any
        transactionHash: Any 
        transactionIndex: Any
        type: Any
    """