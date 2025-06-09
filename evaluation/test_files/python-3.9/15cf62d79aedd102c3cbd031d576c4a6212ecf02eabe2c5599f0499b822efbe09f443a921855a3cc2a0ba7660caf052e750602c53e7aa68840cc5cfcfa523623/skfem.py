import pytest
import numpy as np
from pymor.basic import ExpressionFunction, StationaryProblem, ConstantFunction, RectDomain, LineDomain
from pymor.core.config import config
from pymor.discretizers.builtin.cg import discretize_stationary_cg as discretize_stationary_cg_builtin

def test_skfem1d():
    if not config.HAVE_SCIKIT_FEM:
        pytest.xfail('scikit-fem missing')
    from pymor.discretizers.skfem.cg import discretize_stationary_cg
    p = StationaryProblem(domain=LineDomain([-1, 1], left='dirichlet', right='neumann'), diffusion=ConstantFunction(1.0, 1), advection=ConstantFunction(np.array([-10.0]), 1), rhs=ExpressionFunction('((x[0] - 0.75)**2 < 0.01) * 10', 1), outputs=(('l2', ConstantFunction(1.0, 1)), ('l2_boundary', ExpressionFunction('x[0]+1', 1))))
    (m_skfem, _) = discretize_stationary_cg(p, diameter=1 / 100)
    (m_builtin, _) = discretize_stationary_cg_builtin(p, diameter=1 / 100)
    o_skfem = m_skfem.output()
    o_builtin = m_builtin.output()
    assert np.linalg.norm((o_builtin - o_skfem) / o_builtin) < 0.01

def test_skfem2d():
    if not config.HAVE_SCIKIT_FEM:
        pytest.xfail('scikit-fem missing')
    from pymor.discretizers.skfem.cg import discretize_stationary_cg
    p = StationaryProblem(domain=RectDomain([[-1, -1], [1, 1]], bottom='neumann', right='neumann'), diffusion=ConstantFunction(1.0, 2), advection=ExpressionFunction('[x[1]*100, -x[0]*100]', 2), rhs=ExpressionFunction('(((x[0] - 0.75)**2 + x[1]**2) < 0.01) * 10', 2), outputs=(('l2', ConstantFunction(1.0, 2)), ('l2_boundary', ExpressionFunction('x[1]+1', 2))))
    (m_skfem, _) = discretize_stationary_cg(p, diameter=1 / 50)
    (m_builtin, _) = discretize_stationary_cg_builtin(p, diameter=1 / 50)
    o_skfem = m_skfem.output()
    o_builtin = m_builtin.output()
    assert np.linalg.norm((o_builtin - o_skfem) / o_builtin) < 0.03