from typing import Any, Dict, List, Sequence
from unittest import mock
from unittest.mock import MagicMock
from django.test import TestCase
import pytest
import requests
from eth_account import Account
from hexbytes import HexBytes
from web3.eth import Eth
from web3.types import TxParams
from ..constants import GAS_CALL_DATA_BYTE, NULL_ADDRESS
from ..contracts import get_erc20_contract
from ..ethereum_client import EthereumClient, EthereumClientProvider, EthereumNetwork, FromAddressNotFound, InsufficientFunds, InvalidNonce, SenderAccountNotFoundInNode, TracingManager
from ..exceptions import BatchCallException, ChainIdIsRequired, InvalidERC20Info
from ..utils import get_eth_address_with_key
from .ethereum_test_case import EthereumTestCaseMixin
from .mocks.mock_internal_txs import creation_internal_txs, internal_txs_errored
from .mocks.mock_log_receipts import invalid_log_receipt, log_receipts
from .mocks.mock_trace_block import trace_block_2191709_mock, trace_block_13191781_mock, trace_block_15630274_mock
from .mocks.mock_trace_filter import trace_filter_mock_1
from .mocks.mock_trace_transaction import trace_transaction_mocks
from .utils import deploy_example_erc20, just_test_if_mainnet_node

class TestERC20Module(EthereumTestCaseMixin, TestCase):

    def test_decode_transfer_log(self):
        decoded_logs = self.ethereum_client.erc20.decode_logs(log_receipts + [invalid_log_receipt])
        self.assertEqual(len(decoded_logs), 6)
        self.assertEqual(len([event for event in decoded_logs if 'tokenId' in event['args']]), 2)
        self.assertEqual(len([event for event in decoded_logs if 'value' in event['args']]), 3)
        self.assertEqual(len([event for event in decoded_logs if 'unknown' in event['args']]), 1)
        expected_log_1 = {'address': '0x39C4BFa00b6edecCDd00fA9589E1BE76DE63e862', 'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'), HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'), HexBytes('0x00000000000000000000000064da772dd84965f0ee58174941d78a9dfbccca2e')], 'data': '0x000000000000000000000000000000000000000000000001a055690d9db80000', 'blockNumber': 4357126, 'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'), 'transactionIndex': 14, 'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'), 'logIndex': 14, 'removed': False, 'args': {'from': '0x94E01661eBaef430fE862f958c03200b0F483f27', 'to': '0x64DA772DD84965f0Ee58174941d78a9DfBccca2e', 'value': 30000000000000000000}}
        expected_log_3 = {'address': '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47', 'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'), HexBytes('0x00000000000000000000000099b9f9ba62002a9b43af6e540428277d5e52ef47'), HexBytes('0x00000000000000000000000094e01661ebaef430fe862f958c03200b0f483f27'), HexBytes('0xcc292d3dab2c0fbbf616670ac57ec51162959c2d9cbe938819b6e8bc1c757335')], 'data': '0x', 'blockNumber': 4357126, 'transactionHash': HexBytes('0x21381484d8f69dcd782560d1fd3cd818e743c79767985d01aec7e61c2a7f1de9'), 'transactionIndex': 14, 'blockHash': HexBytes('0x677ada1a306fc50751001bca6eeaa3f5a87a0bf2c9f6fa27899bfbaf999cca4f'), 'logIndex': 17, 'removed': False, 'args': {'from': '0x99b9F9BA62002a9b43aF6e540428277D5E52EF47', 'to': '0x94E01661eBaef430fE862f958c03200b0F483f27', 'tokenId': 92344574081811136966607054691835999266725413506859602442775390826469350798133}}
        expected_log_5 = {'address': '0xe35F3B71CA90eE2606F64b645D8F4f8DCaA914Bf', 'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef')], 'data': '0x0000000000000000000000008683f9c4e856be65f8a38a3a768e8fd6de94d30a000000000000000000000000fd1017c3284a12ac33bc65df12d71721c85931e00000000000000000000000000000000000000000000000000000000000000001', 'blockNumber': 7240557, 'transactionHash': HexBytes('0x1962e296457b16d5221d33623f2db5f617cb54221deb7cfd73611f761ac526a3'), 'transactionIndex': 6, 'blockHash': HexBytes('0xdf3c33d034f1b342820afdfb2612d0794d4a1c15518184d71a047ef1eb151d10'), 'logIndex': 5, 'removed': False, 'args': {'from': '0x8683f9c4e856be65f8a38a3a768e8fd6de94d30a', 'to': '0xfd1017c3284a12ac33bc65df12d71721c85931e0', 'unknown': 1}}
        self.assertEqual(decoded_logs[1], expected_log_1)
        self.assertEqual(decoded_logs[3], expected_log_3)
        self.assertEqual(decoded_logs[5], expected_log_5)

    def test_decode_invalid_transfer_log(self):
        invalid_transfer_logs = [invalid_log_receipt]
        self.assertEqual(self.ethereum_client.erc20.decode_logs(invalid_transfer_logs), [])

    def test_get_name_symbol_balance(self):
        amount = 1000
        address = Account.create().address
        erc20_contract = self.deploy_example_erc20(amount, address)
        token_balance = self.ethereum_client.erc20.get_balance(address, erc20_contract.address)
        self.assertTrue(token_balance, amount)
        another_account = Account.create().address
        token_balance = self.ethereum_client.erc20.get_balance(another_account, erc20_contract.address)
        self.assertEqual(token_balance, 0)
        self.assertTrue(self.ethereum_client.erc20.get_name(erc20_contract.address))
        self.assertTrue(self.ethereum_client.erc20.get_symbol(erc20_contract.address))

    def test_get_balances(self):
        account_address = Account.create().address
        self.assertEqual(self.ethereum_client.erc20.get_balances(account_address, []), [{'token_address': None, 'balance': 0}])
        value = 7
        self.send_ether(account_address, 7)
        self.assertEqual(self.ethereum_client.erc20.get_balances(account_address, []), [{'token_address': None, 'balance': value}])
        tokens_value = 12
        erc20 = self.deploy_example_erc20(tokens_value, account_address)
        self.assertCountEqual(self.ethereum_client.erc20.get_balances(account_address, [erc20.address]), [{'token_address': None, 'balance': value}, {'token_address': erc20.address, 'balance': tokens_value}])
        tokens_value_2 = 19
        erc20_2 = self.deploy_example_erc20(tokens_value_2, account_address)
        self.assertCountEqual(self.ethereum_client.erc20.get_balances(account_address, [erc20.address, erc20_2.address]), [{'token_address': None, 'balance': value}, {'token_address': erc20.address, 'balance': tokens_value}, {'token_address': erc20_2.address, 'balance': tokens_value_2}])
        with mock.patch.object(EthereumClient, 'batch_call_same_function', return_value=[b'\x08\xc3y\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x17Only the proxy can call\x00\x00\x00\x00\x00\x00\x00\x00\x00', 5]):
            token_addresses = ['0x57Ab1E02fEE23774580C119740129eAC7081e9D3', '0x6810e776880C02933D47DB1b9fc05908e5386b96']
            self.assertCountEqual(self.ethereum_client.erc20.get_balances(account_address, token_addresses), [{'token_address': None, 'balance': value}, {'token_address': '0x57Ab1E02fEE23774580C119740129eAC7081e9D3', 'balance': 0}, {'token_address': '0x6810e776880C02933D47DB1b9fc05908e5386b96', 'balance': 5}])

    def test_get_total_transfer_history(self):
        amount = 50
        owner_account = self.create_account(initial_ether=0.01)
        account_1 = self.create_account(initial_ether=0.01)
        account_2 = self.create_account(initial_ether=0.01)
        account_3 = self.create_account(initial_ether=0.01)
        erc20_contract = self.deploy_example_erc20(amount, owner_account.address)
        self.send_tx(erc20_contract.functions.transfer(account_1.address, amount // 2).build_transaction({'from': owner_account.address}), owner_account)
        self.send_tx(erc20_contract.functions.transfer(account_3.address, amount // 2).build_transaction({'from': owner_account.address}), owner_account)
        logs = self.ethereum_client.erc20.get_total_transfer_history([account_1.address])
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['args']['from'], owner_account.address)
        self.assertEqual(logs[0]['args']['to'], account_1.address)
        self.assertEqual(logs[0]['args']['value'], amount // 2)
        log_0_block_number = logs[0]['blockNumber']
        self.send_tx(erc20_contract.functions.transfer(account_2.address, amount // 2).build_transaction({'from': account_1.address}), account_1)
        logs = self.ethereum_client.erc20.get_total_transfer_history([account_1.address], token_address=erc20_contract.address, to_block='latest')
        self.assertEqual(len(logs), 2)
        self.assertEqual(logs[1]['args']['from'], account_1.address)
        self.assertEqual(logs[1]['args']['to'], account_2.address)
        self.assertEqual(logs[1]['args']['value'], amount // 2)
        self.assertGreaterEqual(logs[1]['blockNumber'], log_0_block_number)
        logs = self.ethereum_client.erc20.get_total_transfer_history([account_3.address])
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['args']['from'], owner_account.address)
        self.assertEqual(logs[0]['args']['to'], account_3.address)
        self.assertEqual(logs[0]['args']['value'], amount // 2)
        logs = self.ethereum_client.erc20.get_total_transfer_history([account_2.address, account_3.address])
        self.assertEqual(len(logs), 2)
        logs = self.ethereum_client.erc20.get_total_transfer_history()
        self.assertGreaterEqual(len(logs), 3)

    def test_get_transfer_history(self):
        amount = 1000
        owner_account = self.create_account(initial_ether=0.01)
        receiver_account = self.create_account(initial_ether=0.01)
        receiver2_account = self.create_account(initial_ether=0.01)
        receiver3_account = self.create_account(initial_ether=0.01)
        erc20_contract = self.deploy_example_erc20(amount, owner_account.address)
        block_number = self.w3.eth.block_number
        events = self.ethereum_client.erc20.get_transfer_history(block_number, token_address=erc20_contract.address)
        self.assertEqual(len(events), 1)
        self.send_tx(erc20_contract.functions.transfer(receiver_account.address, amount // 2).build_transaction({'from': owner_account.address}), owner_account)
        self.send_tx(erc20_contract.functions.transfer(receiver2_account.address, amount // 2).build_transaction({'from': owner_account.address}), owner_account)
        self.send_tx(erc20_contract.functions.transfer(receiver3_account.address, amount // 4).build_transaction({'from': receiver_account.address}), receiver_account)
        self.send_tx(erc20_contract.functions.transfer(receiver3_account.address, amount // 4).build_transaction({'from': receiver2_account.address}), receiver2_account)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, token_address=erc20_contract.address)
        self.assertEqual(len(events), 5)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=owner_account.address)
        self.assertEqual(len(events), 2)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver_account.address)
        self.assertEqual(len(events), 1)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver2_account.address)
        self.assertEqual(len(events), 1)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver3_account.address)
        self.assertEqual(len(events), 0)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, to_address=receiver2_account.address)
        self.assertEqual(len(events), 1)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, to_address=receiver3_account.address)
        self.assertEqual(len(events), 2)
        for event in events:
            self.assertEqual(event.args.value, amount // 4)
            self.assertEqual(event.args.to, receiver3_account.address)
        events = self.ethereum_client.erc20.get_transfer_history(block_number, from_address=receiver2_account.address, to_address=receiver3_account.address)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.args.value, amount // 4)
        self.assertEqual(event.args['from'], receiver2_account.address)
        self.assertEqual(event.args.to, receiver3_account.address)

    def test_get_info(self):
        amount = 1
        owner = Account.create().address
        erc20_contract = self.deploy_example_erc20(amount, owner)
        erc20_info = self.ethereum_client.erc20.get_info(erc20_contract.address)
        self.assertEqual(erc20_info.decimals, 18)
        with self.assertRaises(InvalidERC20Info):
            self.ethereum_client.erc20.get_info(Account.create().address)

    def test_send_tokens(self):
        amount = 5
        owner = self.ethereum_test_account
        owner_2 = Account.create()
        erc20 = self.deploy_example_erc20(amount, owner.address)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner.address, erc20.address), amount)
        amount_2 = 3
        self.ethereum_client.erc20.send_tokens(owner_2.address, amount_2, erc20.address, owner.key)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner.address, erc20.address), amount - amount_2)
        self.assertEqual(self.ethereum_client.erc20.get_balance(owner_2.address, erc20.address), amount_2)

class TestTracingManager(EthereumTestCaseMixin, TestCase):

    def test_filter_out_errored_traces(self):
        self.assertEqual(self.ethereum_client.tracing.filter_out_errored_traces([]), [])
        traces = internal_txs_errored
        expected = [{'action': {'from': '0x667dEb5A98f77052cf561658575cF1530Ee42C7a', 'gas': 60066, 'value': 0, 'callType': 'call', 'input': HexBytes('0x6a76120200000000000000000000000090c6e02acc0ff725c0127feac32a53c4b10b03b700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000092000000000000000000000000000000000000000000000000000000000000007a44f84885b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000007600000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000022000000000000000000000000000000000000000000000000000000000000003200000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000050000000000000000000000000000000000000000000000000000000000000006200000000000000000000000002eaa9d77ae4d8f9cdd9faacd44016e746485bddb00000000000000000000000000000000000000000000000000000000000000070000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000006d7f0754ffeb405d23c51ce938289d4835be3b1400000000000000000000000052201ff1720134bbbbb2f6bc97bf3715490ec19b000000000000000000000000ebf1a11532b93a529b5bc942b4baa98647913002000000000000000000000000ebe09eb3411d18f4ff8d859e096c533cac5c6b60000000000000000000000000d6801a1dffcd0a410336ef88def4320d6df1883e0000000000000000000000005b281a6dda0b271e91ae35de655ad301c976edb10000000000000000000000001a32b1734d964b039320c7712aa65b43c826d4dd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000002448ee2641d78cc42d7ad76498917359d961a78300000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000006d7f0754ffeb405d23c51ce938289d4835be3b14000000000000000000000000000000000000000000000000000000000000012c0000000000000000000000001a32b1734d964b039320c7712aa65b43c826d4dd0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000012c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000048e13085b1efda7283d958100e4cbfacb0ce5012000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000012c00000000000000000000000000000000000000000000000000000000000000020000000000000000000000001a32b1734d964b039320c7712aa65b43c826d4dd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041000000000000000000000000667deb5a98f77052cf561658575cf1530ee42c7a00000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000'), 'to': '0x47F61944efdB020829caead65AfF8AC024600580'}, 'blockHash': '0x4c49052fc99be82b91f8a35320826304dfe278dbd7d756edde000d331606358f', 'blockNumber': 4735890, 'result': {'gasUsed': 21838, 'output': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000')}, 'subtraces': 1, 'traceAddress': [], 'transactionHash': '0xf097d5e5dd39a6799fc13dfa49732a115b457386520dc92f99f0135a1d196851', 'transactionPosition': 3, 'type': 'call'}, {'action': {'from': '0x47F61944efdB020829caead65AfF8AC024600580', 'gas': 57726, 'value': 0, 'callType': 'delegatecall', 'input': HexBytes('0x6a76120200000000000000000000000090c6e02acc0ff725c0127feac32a53c4b10b03b700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000092000000000000000000000000000000000000000000000000000000000000007a44f84885b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000007600000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000000000000000000000000000000022000000000000000000000000000000000000000000000000000000000000003200000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000050000000000000000000000000000000000000000000000000000000000000006200000000000000000000000002eaa9d77ae4d8f9cdd9faacd44016e746485bddb00000000000000000000000000000000000000000000000000000000000000070000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000006d7f0754ffeb405d23c51ce938289d4835be3b1400000000000000000000000052201ff1720134bbbbb2f6bc97bf3715490ec19b000000000000000000000000ebf1a11532b93a529b5bc942b4baa98647913002000000000000000000000000ebe09eb3411d18f4ff8d859e096c533cac5c6b60000000000000000000000000d6801a1dffcd0a410336ef88def4320d6df1883e0000000000000000000000005b281a6dda0b271e91ae35de655ad301c976edb10000000000000000000000001a32b1734d964b039320c7712aa65b43c826d4dd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000002448ee2641d78cc42d7ad76498917359d961a78300000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000000000000000006d7f0754ffeb405d23c51ce938289d4835be3b14000000000000000000000000000000000000000000000000000000000000012c0000000000000000000000001a32b1734d964b039320c7712aa65b43c826d4dd0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000012c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000048e13085b1efda7283d958100e4cbfacb0ce5012000000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000012c00000000000000000000000000000000000000000000000000000000000000020000000000000000000000001a32b1734d964b039320c7712aa65b43c826d4dd0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000041000000000000000000000000667deb5a98f77052cf561658575cf1530ee42c7a00000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000'), 'to': '0xb6029EA3B2c51D09a50B53CA8012FeEB05bDa35A'}, 'blockHash': '0x4c49052fc99be82b91f8a35320826304dfe278dbd7d756edde000d331606358f', 'blockNumber': 4735890, 'result': {'gasUsed': 20369, 'output': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000')}, 'subtraces': 1, 'traceAddress': [0], 'transactionHash': '0xf097d5e5dd39a6799fc13dfa49732a115b457386520dc92f99f0135a1d196851', 'transactionPosition': 3, 'type': 'call'}]
        self.assertEqual(self.ethereum_client.tracing.filter_out_errored_traces(traces), expected)
        traces = [{'traceAddress': []}, {'traceAddress': [0]}, {'traceAddress': [0, 0]}, {'error': 'reverted', 'traceAddress': [0, 0, 0]}, {'traceAddress': [0, 0, 0, 0]}, {'traceAddress': [0, 0, 0, 1]}, {'traceAddress': [0, 0, 1]}, {'traceAddress': [0, 0, 1, 0]}, {'error': 'reverted', 'traceAddress': [0, 0, 1, 0, 0]}, {'traceAddress': [0, 0, 1, 0, 1]}, {'traceAddress': [0, 0, 1, 0, 2]}, {'error': 'reverted', 'traceAddress': [0, 0, 1, 0, 3]}, {'traceAddress': [0, 0, 2]}]
        expected = [{'traceAddress': []}, {'traceAddress': [0]}, {'traceAddress': [0, 0]}, {'traceAddress': [0, 0, 1]}, {'traceAddress': [0, 0, 1, 0]}, {'traceAddress': [0, 0, 1, 0, 1]}, {'traceAddress': [0, 0, 1, 0, 2]}, {'traceAddress': [0, 0, 2]}]
        self.assertEqual(sorted(traces, key=lambda trace: trace['traceAddress']), traces)
        self.assertEqual(self.ethereum_client.tracing.filter_out_errored_traces(traces), expected)

    @mock.patch.object(TracingManager, 'trace_transaction', return_value=internal_txs_errored)
    def test_get_previous_trace(self, trace_transaction_mock: MagicMock):
        self.assertEqual(self.ethereum_client.tracing.get_previous_trace('0x12', [0, 0])['traceAddress'], [0])
        self.assertEqual(self.ethereum_client.tracing.get_previous_trace('0x12', [0, 0], number_traces=2)['traceAddress'], [])
        self.assertEqual(self.ethereum_client.tracing.get_previous_trace('0x12', [0, 0], skip_delegate_calls=True)['traceAddress'], [])
        self.assertIsNone(self.ethereum_client.tracing.get_previous_trace('0x12', [0, 0], number_traces=3))
        self.assertEqual(self.ethereum_client.tracing.get_previous_trace('0x12', [0, 0, 0], skip_delegate_calls=True)['traceAddress'], [0, 0])

    @mock.patch.object(TracingManager, 'trace_transaction', return_value=creation_internal_txs)
    def test_get_next_traces(self, trace_transaction_mock: MagicMock):

        def trace_addresses(traces: Sequence[Dict[str, Any]]) -> List[List[int]]:
            return [trace['traceAddress'] for trace in traces]
        self.assertEqual(trace_addresses(self.ethereum_client.tracing.get_next_traces('0x12', [])), [[0], [1]])
        self.assertEqual(trace_addresses(self.ethereum_client.tracing.get_next_traces('0x12', [], remove_delegate_calls=True)), [[1]])
        self.assertEqual(trace_addresses(self.ethereum_client.tracing.get_next_traces('0x12', [], remove_calls=True)), [[0]])
        self.assertEqual(trace_addresses(self.ethereum_client.tracing.get_next_traces('0x12', [], remove_delegate_calls=True, remove_calls=True)), [])
        self.assertEqual(self.ethereum_client.tracing.get_next_traces('0x12', [0]), [])
        self.assertEqual(trace_addresses(self.ethereum_client.tracing.get_next_traces('0x12', [1])), [[1, 0]])

    def test_trace_filter(self):
        with self.assertRaisesMessage(AssertionError, 'at least'):
            self.ethereum_client.tracing.trace_filter()
        with self.assertRaisesMessage(ValueError, 'The method trace_filter does not exist/is not available'):
            self.ethereum_client.tracing.trace_filter(to_address=[Account.create().address])

    @mock.patch.object(requests.Response, 'json')
    def test_raw_batch_request(self, session_post_mock: MagicMock):
        session_post_mock.return_value = {'jsonrpc': '2.0', 'error': {'code': 0, 'message': "you can't send more than 1000 requests in a batch"}, 'id': None}
        payload = [{'id': 0, 'jsonrpc': '2.0', 'method': 'eth_getTransactionByHash', 'params': '0x5afea3f32970a22f4e63a815c174fa989e3b659826e5f52496662bb256baf3b2'}, {'id': 1, 'jsonrpc': '2.0', 'method': 'eth_getTransactionByHash', 'params': '0x12ab96991ddd4ac55c28ace4e7b59bc64c514b55747e1b0ea3f5b269fbb39f6b'}]
        with self.assertRaisesMessage(ValueError, 'Batch request error: {\'jsonrpc\': \'2.0\', \'error\': {\'code\': 0, \'message\': "you can\'t send more than 1000 requests in a batch"}, \'id\': None}'):
            list(self.ethereum_client.raw_batch_request(payload))
        session_post_mock.return_value = [{'jsonrpc': '2.0', 'id': None, 'error': {'code': -32000, 'message': 'batch length does not support more than 500'}}]
        with self.assertRaisesMessage(ValueError, "Problem with payload=`{'id': 0, 'jsonrpc': '2.0', 'method': 'eth_getTransactionByHash', 'params': '0x5afea3f32970a22f4e63a815c174fa989e3b659826e5f52496662bb256baf3b2'}` result={'jsonrpc': '2.0', 'id': None, 'error': {'code': -32000, 'message': 'batch length does not support more than 500'}}"):
            list(self.ethereum_client.raw_batch_request(payload))
        session_post_mock.return_value = [{'jsonrpc': '2.0', 'id': 0, 'result': {'blockHash': '0x13e9e3262d9cf1c4d07d7324d95e6bddf27f07d7bddbdcc7df4e4ffb42a2e921', 'blockNumber': '0xa81a59', 'from': '0x136ec956eb32364f5016f3f84f56dbff59c6ead5', 'gas': '0x493e0', 'gasPrice': '0x3b9aca0e', 'maxPriorityFeePerGas': '0x3b9aca00', 'maxFeePerGas': '0x3b9aca1e', 'hash': '0x92898917d7bd7a51d40a903f4c55ae988cbac7c661c3e271c54bbda21415501b', 'input': '0x8ea59e1de547ab59caab9379b4b307450a29a0137c7dbbfc7b18c3cd6179d927efbab9ee', 'nonce': '0x1242f', 'to': '0x7e22c795325e76306920293f62a02f353536280b', 'transactionIndex': '0x1e', 'value': '0x0', 'type': '0x2', 'accessList': [], 'chainId': '0x4', 'v': '0x1', 'r': '0x5aaaa2a32326ca4add9a602ffba968c3d991219fde93a2531eb7a82fc61919ed', 's': '0x1c4bff2abcc671ad2a1dd09f92a9720ac595138c666e59153711056811c1c95c'}}]
        results = list(self.ethereum_client.raw_batch_request(payload, batch_size=1))
        self.assertEqual(len(results), 2)

class TestEthereumNetwork(EthereumTestCaseMixin, TestCase):

    def test_unknown_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(123456789), EthereumNetwork.UNKNOWN)

    def test_mainnet_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(1), EthereumNetwork.MAINNET)

    def test_rinkeby_ethereum_network_name(self):
        self.assertEqual(EthereumNetwork(4), EthereumNetwork.RINKEBY)

class TestEthereumClient(EthereumTestCaseMixin, TestCase):

    def test_ethereum_client_str(self):
        self.assertTrue(str(self.ethereum_client))

    def test_current_block_number(self):
        self.assertGreaterEqual(self.ethereum_client.current_block_number, 0)

    def test_get_transaction(self):
        to = Account.create().address
        value = 123
        tx_hash = self.send_ether(to, value)
        tx = self.ethereum_client.get_transaction(tx_hash)
        self.assertEqual(tx.to, to)
        self.assertEqual(tx.value, value)
        block = self.ethereum_client.get_block(tx.blockNumber)
        self.assertEqual(block.number, tx.blockNumber)

    def test_get_transactions(self):
        self.assertEqual(self.ethereum_client.get_transactions([]), [])
        to = Account.create().address
        values = [123, 234, 567]
        tx_hashes = [self.send_ether(to, values[i]) for i in range(3)]
        txs = self.ethereum_client.get_transactions(tx_hashes)
        for (i, tx) in enumerate(txs):
            self.assertEqual(tx['to'], to)
            self.assertEqual(tx['value'], values[i])
        self.assertEqual(self.ethereum_client.get_transaction_receipts([]), [])
        receipts = self.ethereum_client.get_transaction_receipts(tx_hashes)
        for (i, receipt) in enumerate(receipts):
            self.assertEqual(receipt['status'], 1)
            self.assertGreaterEqual(receipt['gasUsed'], 21000)

    def test_check_tx_with_confirmations(self):
        value = 1
        (to, _) = get_eth_address_with_key()
        tx_hash = self.ethereum_client.send_eth_to(self.ethereum_test_account.key, to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))
        _ = self.ethereum_client.send_eth_to(self.ethereum_test_account.key, to=to, gas_price=self.gas_price, value=value)
        self.assertFalse(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))
        _ = self.ethereum_client.send_eth_to(self.ethereum_test_account.key, to=to, gas_price=self.gas_price, value=value)
        self.assertTrue(self.ethereum_client.check_tx_with_confirmations(tx_hash, 2))

    def test_estimate_gas(self):
        send_ether_gas = 21000
        from_ = self.ethereum_test_account.address
        (to, _) = get_eth_address_with_key()
        gas = self.ethereum_client.estimate_gas(to, from_=from_, value=5, data=None, block_identifier='pending')
        self.assertEqual(gas, send_ether_gas)
        gas = self.ethereum_client.estimate_gas(to, from_=from_, value=5, data=b'')
        self.assertEqual(gas, send_ether_gas)
        gas = self.ethereum_client.estimate_gas(to, from_=from_, value=5, data=None)
        self.assertEqual(gas, send_ether_gas)

    def test_estimate_gas_with_erc20(self):
        send_ether_gas = 21000
        amount_tokens = 5000
        amount_to_send = amount_tokens // 2
        from_account = self.ethereum_test_account
        from_ = from_account.address
        (to, _) = get_eth_address_with_key()
        erc20_contract = self.deploy_example_erc20(amount_tokens, from_)
        transfer_tx = erc20_contract.functions.transfer(to, amount_to_send).build_transaction({'from': from_})
        data = transfer_tx['data']
        gas = self.ethereum_client.estimate_gas(erc20_contract.address, from_=from_, value=0, data=data, block_identifier='pending')
        self.assertGreater(gas, send_ether_gas)
        self.send_tx(transfer_tx, from_account)
        token_balance = self.ethereum_client.erc20.get_balance(to, erc20_contract.address)
        self.assertTrue(token_balance, amount_to_send)
        gas2 = self.ethereum_client.estimate_gas(erc20_contract.address, from_=from_, value=0, data=data, block_identifier='pending')
        self.assertLess(gas2, gas)

    def test_get_ethereum_network(self):
        self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.GANACHE)
        with mock.patch.object(Eth, 'chain_id', return_value=1, new_callable=mock.PropertyMock):
            self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.GANACHE)
            self.ethereum_client.get_chain_id.cache_clear()
            self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.MAINNET)
            self.ethereum_client.get_chain_id.cache_clear()
        with mock.patch.object(Eth, 'chain_id', return_value=4, new_callable=mock.PropertyMock):
            self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.RINKEBY)
            self.ethereum_client.get_chain_id.cache_clear()
        with mock.patch.object(Eth, 'chain_id', return_value=4815162342, new_callable=mock.PropertyMock):
            self.assertEqual(self.ethereum_client.get_network(), EthereumNetwork.UNKNOWN)
            self.ethereum_client.get_chain_id.cache_clear()

    def test_get_nonce(self):
        address = Account.create().address
        nonce = self.ethereum_client.get_nonce_for_account(address)
        self.assertEqual(nonce, 0)
        nonce = self.ethereum_client.get_nonce_for_account(address, block_identifier='pending')
        self.assertEqual(nonce, 0)

    def test_estimate_data_gas(self):
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('')), 0)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x00')), 4)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x000204')), 4 + GAS_CALL_DATA_BYTE * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x050204')), GAS_CALL_DATA_BYTE * 3)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x0502040000')), GAS_CALL_DATA_BYTE * 3 + 4 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x050204000001')), GAS_CALL_DATA_BYTE * 4 + 4 * 2)
        self.assertEqual(self.ethereum_client.estimate_data_gas(HexBytes('0x00050204000001')), 4 + GAS_CALL_DATA_BYTE * 4 + 4 * 2)

    def test_provider_singleton(self):
        ethereum_client1 = EthereumClientProvider()
        ethereum_client2 = EthereumClientProvider()
        self.assertEqual(ethereum_client1, ethereum_client2)

    def test_send_eth_to(self):
        (address, _) = get_eth_address_with_key()
        value = 1
        self.ethereum_client.send_eth_to(self.ethereum_test_account.key, address, self.gas_price, value)
        self.assertEqual(self.ethereum_client.get_balance(address), value)

    def test_send_eth_without_key(self):
        with self.settings(SAFE_FUNDER_PRIVATE_KEY=None):
            self.test_send_eth_to()

    def test_send_transaction(self):
        account = self.ethereum_test_account
        address = account.address
        (to, _) = get_eth_address_with_key()
        value = 1
        tx = {'to': to, 'value': value, 'gas': 23000, 'gasPrice': self.gas_price, 'nonce': self.ethereum_client.get_nonce_for_account(address)}
        with self.assertRaises(FromAddressNotFound):
            self.ethereum_client.send_transaction(tx)
        tx['from'] = Account.create().address
        with self.assertRaises(SenderAccountNotFoundInNode):
            self.ethereum_client.send_transaction(tx)
        tx['from'] = address
        self.ethereum_client.send_transaction(tx)
        self.assertEqual(self.ethereum_client.get_balance(to), 1)
        with self.assertRaises(InvalidNonce):
            self.ethereum_client.send_transaction(tx)
        tx['value'] = self.ethereum_client.get_balance(address) + 1
        tx['nonce'] = self.ethereum_client.get_nonce_for_account(address)
        with self.assertRaises(InsufficientFunds):
            self.ethereum_client.send_transaction(tx)

    def test_send_unsigned_transaction(self):
        account = self.ethereum_test_account
        address = account.address
        (to, _) = get_eth_address_with_key()
        value = 4
        tx = {'to': to, 'value': value, 'gas': 23000}
        with self.assertRaisesMessage(ValueError, 'Ethereum account was not configured'):
            self.ethereum_client.send_unsigned_transaction(tx)
        self.ethereum_client.send_unsigned_transaction(tx, public_key=address)
        self.assertEqual(self.ethereum_client.get_balance(to), value)
        first_nonce = tx['nonce']
        self.assertGreaterEqual(first_nonce, 0)
        with self.assertRaisesMessage(InvalidNonce, 'correct nonce'):
            self.ethereum_client.send_unsigned_transaction(tx, public_key=address)
        self.ethereum_client.send_unsigned_transaction(tx, public_key=address, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 1)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 2)
        tx['nonce'] = first_nonce
        self.ethereum_client.send_unsigned_transaction(tx, public_key=address, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 2)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 3)

    @pytest.mark.xfail(reason='Last ganache-cli version broke the test')
    def test_send_unsigned_transaction_with_private_key(self):
        account = self.create_account(initial_ether=0.1)
        key = account.key
        (to, _) = get_eth_address_with_key()
        value = 4
        tx = {'to': to, 'value': value, 'gas': 23000, 'gasPrice': self.gas_price}
        self.ethereum_client.send_unsigned_transaction(tx, private_key=key)
        self.assertEqual(self.ethereum_client.get_balance(to), value)
        first_nonce = tx['nonce']
        self.assertGreaterEqual(first_nonce, 0)
        with self.assertRaisesMessage(InvalidNonce, 'correct nonce'):
            self.ethereum_client.send_unsigned_transaction(tx, private_key=key)
        self.ethereum_client.send_unsigned_transaction(tx, private_key=key, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 1)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 2)
        tx['nonce'] = first_nonce
        self.ethereum_client.send_unsigned_transaction(tx, private_key=key, retry=True)
        self.assertEqual(tx['nonce'], first_nonce + 2)
        self.assertEqual(self.ethereum_client.get_balance(to), value * 3)

    def test_wait_for_tx_receipt(self):
        value = 1
        to = Account.create().address
        tx_hash = self.ethereum_client.send_eth_to(self.ethereum_test_account.key, to=to, gas_price=self.gas_price, value=value)
        receipt1 = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=None)
        receipt2 = self.ethereum_client.get_transaction_receipt(tx_hash, timeout=20)
        self.assertIsNotNone(receipt1)
        self.assertEqual(receipt1, receipt2)
        fake_tx_hash = self.w3.keccak(0)
        self.assertIsNone(self.ethereum_client.get_transaction_receipt(fake_tx_hash, timeout=None))
        self.assertIsNone(self.ethereum_client.get_transaction_receipt(fake_tx_hash, timeout=1))

    def test_batch_call(self):
        account_address = Account.create().address
        tokens_value = 12
        tokens_value_2 = 25
        erc20 = self.deploy_example_erc20(tokens_value, account_address)
        erc20_2 = self.deploy_example_erc20(tokens_value_2, account_address)
        for batch_call_manager in (self.ethereum_client, self.ethereum_client.batch_call_manager):
            with self.subTest(batch_call_manager=batch_call_manager):
                results = batch_call_manager.batch_call([erc20.functions.decimals(), erc20.functions.symbol(), erc20.functions.balanceOf(account_address)])
                (decimals, symbol, balance_of) = results
                self.assertEqual(decimals, erc20.functions.decimals().call())
                self.assertEqual(symbol, erc20.functions.symbol().call())
                self.assertEqual(balance_of, tokens_value)
                results = batch_call_manager.batch_call_same_function(erc20.functions.balanceOf(account_address), [erc20.address, erc20_2.address])
                self.assertEqual([tokens_value, tokens_value_2], results)
                invalid_erc20 = get_erc20_contract(self.ethereum_client.w3, Account.create().address)
                with self.assertRaises(BatchCallException):
                    batch_call_manager.batch_call([invalid_erc20.functions.decimals(), invalid_erc20.functions.symbol(), erc20.functions.balanceOf(account_address), invalid_erc20.functions.balanceOf(account_address)])
                self.assertEqual(batch_call_manager.batch_call([invalid_erc20.functions.decimals(), invalid_erc20.functions.symbol(), erc20.functions.balanceOf(account_address), invalid_erc20.functions.balanceOf(account_address)], raise_exception=False), [None, None, tokens_value, None])
                with self.assertRaises(BatchCallException):
                    batch_call_manager.batch_call([erc20.functions.decimals(), erc20.functions.transfer(NULL_ADDRESS, 1), erc20.functions.symbol(), erc20.functions.balanceOf(account_address)], raise_exception=True)

    def test_get_blocks(self):
        self.assertEqual(self.ethereum_client.get_blocks([]), [])
        to = Account.create().address
        value = 345
        for _ in range(3):
            self.send_ether(to, value)
        block_numbers = [self.ethereum_client.current_block_number - i for i in range(3)]
        blocks = self.ethereum_client.get_blocks(block_numbers, full_transactions=True)
        block_hashes = [block['hash'] for block in blocks]
        block_hashes_hex = [block_hash.hex() for block_hash in block_hashes]
        for (block_number, block) in zip(block_numbers, blocks):
            self.assertEqual(block['number'], block_number)
            self.assertEqual(len(block['hash']), 32)
            self.assertEqual(len(block['parentHash']), 32)
            self.assertGreaterEqual(len(block['transactions']), 0)
        blocks = self.ethereum_client.get_blocks(block_hashes, full_transactions=True)
        for (block_number, block) in zip(block_numbers, blocks):
            self.assertEqual(block['number'], block_number)
            self.assertEqual(len(block['hash']), 32)
            self.assertEqual(len(block['parentHash']), 32)
            self.assertGreaterEqual(len(block['transactions']), 0)
        blocks = self.ethereum_client.get_blocks(block_hashes_hex, full_transactions=True)
        for (block_number, block) in zip(block_numbers, blocks):
            self.assertEqual(block['number'], block_number)
            self.assertEqual(len(block['hash']), 32)
            self.assertEqual(len(block['parentHash']), 32)
            self.assertGreaterEqual(len(block['transactions']), 0)

    def test_is_contract(self):
        self.assertFalse(self.ethereum_client.is_contract(self.ethereum_test_account.address))
        erc20 = deploy_example_erc20(self.ethereum_client.w3, 2, self.ethereum_test_account.address)
        self.assertTrue(self.ethereum_client.is_contract(erc20.address))

    def test_is_eip1559_supported(self):
        self.assertTrue(self.ethereum_client.is_eip1559_supported())

    def test_set_eip1559_fees(self):
        with mock.patch.object(EthereumClient, 'estimate_fee_eip1559', return_value=(2, 5)):
            tx: TxParams = {'to': Account.create(), 'value': 1, 'gasPrice': 5}
            eip_1559_tx = self.ethereum_client.set_eip1559_fees(tx)
            self.assertIn('gasPrice', tx)
            self.assertNotIn('gasPrice', eip_1559_tx)
            self.assertEqual(eip_1559_tx['chainId'], self.ethereum_client.get_network().value)
            self.assertEqual(eip_1559_tx['maxPriorityFeePerGas'], 5)
            self.assertEqual(eip_1559_tx['maxFeePerGas'], 7)

class TestEthereumClientWithMainnetNode(EthereumTestCaseMixin, TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        mainnet_node = just_test_if_mainnet_node()
        cls.ethereum_client = EthereumClient(mainnet_node)

    def test_is_eip1559_supported(self):
        self.assertTrue(self.ethereum_client.is_eip1559_supported())

    def test_estimate_fee_eip1559(self):
        """
        EIP1559 is still not supported on Ganache
        """
        (base_fee_per_gas, max_priority_fee_per_gas) = self.ethereum_client.estimate_fee_eip1559()
        self.assertGreater(base_fee_per_gas, 0)
        self.assertGreaterEqual(max_priority_fee_per_gas, 0)

    def test_send_unsigned_transaction(self):
        random_address = Account.create().address
        random_sender_account = Account.create()
        tx = {'to': random_address, 'value': 0, 'data': b'', 'gas': 25000, 'gasPrice': self.ethereum_client.w3.eth.gas_price}
        with self.assertRaises(ChainIdIsRequired):
            self.ethereum_client.send_unsigned_transaction(tx, private_key=random_sender_account.key)
        tx['chainId'] = 1
        with self.assertRaises(InsufficientFunds):
            self.ethereum_client.send_unsigned_transaction(tx, private_key=random_sender_account.key)

    def test_trace_block(self):
        block_numbers = [13191781, 2191709, 15630274]
        block_mocks = [trace_block_13191781_mock, trace_block_2191709_mock, trace_block_15630274_mock]
        for (block_number, trace_block_mock) in zip(block_numbers, block_mocks):
            with self.subTest(block_number=block_number):
                self.assertEqual(self.ethereum_client.tracing.trace_block(block_number), trace_block_mock)

    def test_trace_blocks(self):
        block_numbers = [13191781, 2191709, 15630274]
        block_mocks = [trace_block_13191781_mock, trace_block_2191709_mock, trace_block_15630274_mock]
        self.assertEqual(self.ethereum_client.tracing.trace_blocks(block_numbers), block_mocks)

    def test_trace_transaction(self):
        for tx_hash in ['0x0b04589bdc11585fb98f270b1bfeff0fb3bbb3c56d35b104f62d8115d6f7c57f', '0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0']:
            with self.subTest(tx_hash=tx_hash):
                self.assertEqual(self.ethereum_client.tracing.trace_transaction(tx_hash), trace_transaction_mocks[tx_hash])

    def test_trace_transactions(self):
        tx_hashes = ['0x0b04589bdc11585fb98f270b1bfeff0fb3bbb3c56d35b104f62d8115d6f7c57f', '0xf325b4e52d0649593e8c82f35bd389c13c13b21b61bc17de295979a21e5cfdc0', '0xc27273dc6e631d275baa527e1b07cd9097887317c26034bf8ea7bbe38c9353f0']
        self.assertEqual(self.ethereum_client.tracing.trace_transactions(tx_hashes), [trace_transaction_mocks[tx_hash] for tx_hash in tx_hashes])

    def test_trace_filter(self):
        safe_1_3_0_address = '0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552'
        self.assertListEqual(self.ethereum_client.tracing.trace_filter(from_block=12504268, to_block=12504268, to_address=[safe_1_3_0_address]), trace_filter_mock_1)