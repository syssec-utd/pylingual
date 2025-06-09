"""Derived from `passed_tests` notebook test-2"""
from carbon import CarbonSimulatorUI

def test_add_linked_pos_concentrated_on_one_point():
    """
    Derived from `passed_tests` notebook test-2
    """
    Sim = CarbonSimulatorUI(pair='USDC/ETH', verbose=True)
    assert Sim.add_strategy('ETH', 100, 2000, 2000, 0, 1000, 1000)['orders'].to_dict() == {'id': {0: 0, 1: 1}, 'pair': {0: 'USDCETH', 1: 'USDCETH'}, 'tkn': {0: 'ETH', 1: 'USDC'}, 'y_int': {0: 100.0, 1: 0.0}, 'y': {0: 100.0, 1: 0.0}, 'y_unit': {0: 'ETH', 1: 'USDC'}, 'p_start': {0: 2000.0, 1: 1000.0}, 'p_end': {0: 2000.0, 1: 1000.0}, 'disabled': {0: False, 1: False}, 'p_marg': {0: 2000.0000000000002, 1: 1000.0000000000002}, 'p_unit': {0: 'ETH per USDC', 1: 'ETH per USDC'}, 'lid': {0: 1, 1: 0}}

def test_amm_cannot_buy_eth_with_no_usdc():
    """
    Derived from `passed_tests` notebook test-2
    """
    Sim = CarbonSimulatorUI(pair='USDC/ETH', verbose=True)
    Sim.add_strategy('ETH', 100, 2000, 2000, 0, 1000, 1000)
    result = Sim.amm_buys('ETH', 10)
    assert result['success'] is False
    assert result['error'] == 'token USDC has no non-empty liquidity positions'

def test_amm_can_sell_eth_at_curve_price():
    """
    Derived from `passed_tests` notebook test-1
    """
    Sim = CarbonSimulatorUI(pair='USDC/ETH', verbose=True)
    Sim.add_strategy('ETH', 100, 2000, 2000, 0, 1000, 1000)
    result = Sim.amm_sells('ETH', 10)
    assert result['success'] is True
    assert result['trades'].to_dict() == {'uid': {0: '0'}, 'id': {0: 0}, 'subid': {0: 'A'}, 'note': {0: 'AMM sells 10ETH buys 0USDC'}, 'aggr': {0: True}, 'exec': {0: True}, 'limitfail': {0: None}, 'amt1': {0: 10.0}, 'tkn1': {0: 'ETH'}, 'amt2': {0: 0.005}, 'tkn2': {0: 'USDC'}, 'pair': {0: 'USDCETH'}, 'routeix': {0: '[0]'}, 'nroutes': {0: 1}, 'price': {0: 2000.0}, 'p_unit': {0: 'ETH per USDC'}, 'partial': {0: True}}

def test_amm_cannot_sell_with_insufficient_liquidity_1():
    """
    Derived from `passed_tests` notebook test-3
    """
    Sim = CarbonSimulatorUI(pair='ETH/USDC', verbose=True)
    Sim.add_strategy('ETH', 100, 2000, 2000, 0, 1000, 1000)
    result = Sim.amm_sells('ETH', 200)
    assert result['success'] is False
    assert result['error'] == 'Insufficient liquidity across all user positions to support this trade.'

def test_amm_cannot_sell_with_insufficient_liquidity_2():
    """
    Derived from `passed_tests` notebook test-3
    """
    Sim = CarbonSimulatorUI(pair='ETH/USDC', verbose=True)
    Sim.add_strategy('ETH', 100, 2000, 2000, 0, 1000, 1000)
    Sim.amm_sells('ETH', 10)
    result = Sim.amm_sells('ETH', 90.0001)
    assert result['success'] is False
    assert result['error'] == 'Insufficient liquidity across all user positions to support this trade.'

def test_amm_sells_both_directions():
    """
    Derived from `passed_tests` notebook test-12
    """
    Sim = CarbonSimulatorUI(pair='ETH/USDC', verbose=True)
    Sim.add_strategy('ETH', 100, 2000, 2000, 0, 1000, 1000)
    result = Sim.amm_sells('ETH', 100)
    assert result['success'] is True
    assert result['trades']['price'].astype(float).mean() == 2000.0
    result = Sim.amm_sells('USDC', 200000)
    assert result['success'] is True
    assert result['trades']['price'].astype(float).mean() == 1000.0