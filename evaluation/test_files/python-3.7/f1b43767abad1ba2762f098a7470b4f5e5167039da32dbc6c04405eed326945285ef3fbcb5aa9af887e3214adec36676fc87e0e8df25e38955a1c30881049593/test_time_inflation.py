"""Tests for `primpy.time.inflation` module."""
import pytest
import numpy as np
from primpy.potentials import QuadraticPotential
from primpy.time.inflation import InflationEquationsT

@pytest.mark.parametrize('K', [-1, 0, +1])
def test_basic_methods(K):
    eq = InflationEquationsT(K=K, potential=QuadraticPotential(Lambda=1))
    assert hasattr(eq, 'phi')
    assert hasattr(eq, 'dphidt')
    y0 = np.zeros(len(eq.idx))
    assert eq.H2(x=0, y=y0) == -K
    y1 = np.ones(len(eq.idx))
    assert eq.H2(x=1, y=y1) == 1 / 3 - K * np.exp(-2)
    assert eq.H(x=1, y=y1) == np.sqrt(1 / 3 - K * np.exp(-2))
    assert eq.w(x=1, y=y1) == 0
    assert eq.inflating(x=1, y=y1) == -0.5