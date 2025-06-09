import numpy as np
import pandas as pd
import cvxpy as cvx
import seaborn as sns
import matplotlib.pyplot as plt
from numba import jit
from enum import Enum
from typing import Tuple, Optional

class PortfolioObjective(Enum):
    MIN_VAR = 1
    MAX_LOG_UTIL = 2
    EQUAL_RISK_CONTRIBUTION = 3
    RISK_PARITY_ALT = 4
    MAX_DIVERSIFICATION = 5

def maximize_portfolio_objective_qp(portfolio_objective: PortfolioObjective, covar: np.ndarray, means: np.ndarray=None, weight_mins: np.ndarray=None, weight_maxs: np.ndarray=None, is_gross_notional_one: bool=True, is_long_only: bool=True, exposure_budget_eq: Optional[Tuple[np.ndarray, float]]=None, gamma: float=1.0) -> np.ndarray:
    """
    cvx solution for max objective
    subject to linear constraints
         1. weight_min <= w <= weight_max
         2. sum(w) = 1: is_gross_notional_one true or false
         3. exposure_budget_eq[0]^t*w = exposure_budget_eq[1]
    """
    n = covar.shape[0]
    w = cvx.Variable(n)
    portfolio_var = cvx.quad_form(w, covar)
    if portfolio_objective == PortfolioObjective.MIN_VAR:
        objective_fun = -portfolio_var
    elif portfolio_objective == PortfolioObjective.MAX_LOG_UTIL:
        if means is None:
            raise ValueError(f'means must be given')
        objective_fun = means.T @ w - 0.5 * gamma * portfolio_var
    else:
        raise ValueError(f'unknown portfolio_objective')
    objective = cvx.Maximize(objective_fun)
    constraints = []
    if is_gross_notional_one:
        constraints = constraints + [cvx.sum(w) == 1]
    if is_long_only:
        constraints = constraints + [w >= 0]
    if weight_mins is not None:
        constraints = constraints + [w >= weight_mins]
    if weight_maxs is not None:
        constraints = constraints + [w <= weight_maxs]
    if exposure_budget_eq is not None:
        constraints = constraints + [exposure_budget_eq[0] @ w == exposure_budget_eq[1]]
    problem = cvx.Problem(objective, constraints)
    problem.solve()
    optimal_weights = w.value
    if optimal_weights is None:
        raise ValueError(f'not solved')
    return optimal_weights

def max_qp_portfolio_vol_target(portfolio_objective: PortfolioObjective, covar: np.ndarray, means: np.ndarray=None, weight_min: np.ndarray=None, weight_max: np.ndarray=None, is_gross_notional_one: bool=True, is_long_only: bool=True, exposure_budget_eq: Tuple[np.ndarray, float]=None, vol_target: float=0.12) -> np.ndarray:
    max_iter = 20
    sol_tol = 1e-05

    def f(lambda_n: float) -> float:
        w_n = maximize_portfolio_objective_qp(portfolio_objective=portfolio_objective, covar=covar, means=means, weight_mins=weight_min, weight_maxs=weight_max, is_gross_notional_one=is_gross_notional_one, is_long_only=is_long_only, exposure_budget_eq=exposure_budget_eq, gamma=lambda_n)
        print('lambda_n=' + str(lambda_n))
        print_portfolio_outputs(optimal_weights=w_n, covar=covar, means=means)
        target = w_n.T @ covar @ w_n - vol_target ** 2
        return target
    cov_inv = np.linalg.inv(covar)
    e = np.ones(covar.shape[0])
    if means is not None:
        a = np.sqrt(e.T @ cov_inv @ e / (2 * vol_target ** 2))
        b = np.sqrt(means.T @ cov_inv @ means / (2 * vol_target ** 2))
    else:
        a = np.sqrt(e.T @ cov_inv @ e / (2 * vol_target ** 2))
        b = 100
    f_a = f(a)
    f_b = f(b)
    print(f'initial: {[f_a, f_b]}')
    if np.sign(f_a) == np.sign(f_b):
        raise ValueError(f'the same signs: {[f_a, f_b]}')
    lambda_n = 0.5 * (a + b)
    for it in range(max_iter):
        lambda_n = 0.5 * (a + b)
        f_n = f(lambda_n)
        if np.abs(f_n) <= sol_tol or np.abs((b - a) / 2.0) < sol_tol:
            break
        if np.sign(f_n) == np.sign(f_a):
            a = lambda_n
            f_a = f_n
        else:
            b = lambda_n
        print('it=' + str(it))
    w_n = maximize_portfolio_objective_qp(portfolio_objective=portfolio_objective, covar=covar, means=means, weight_mins=weight_min, weight_maxs=weight_max, is_gross_notional_one=is_gross_notional_one, is_long_only=is_long_only, exposure_budget_eq=exposure_budget_eq, gamma=lambda_n)
    print_portfolio_outputs(optimal_weights=w_n, covar=covar, means=means)
    return w_n

def max_portfolio_sharpe_qp(covar: np.ndarray, means: np.ndarray, weight_mins: np.ndarray=None, weight_maxs: np.ndarray=None, is_gross_notional_one: bool=False, is_long_only: bool=True, exposure_budget_eq: Tuple[np.ndarray, float]=None, exposure_budget_le: Tuple[np.ndarray, float]=None, is_print_log: bool=True) -> np.ndarray:
    """
    max means^t*w / sqrt(w^t @ covar @ w)
    subject to
     1. weight_min <= w <= weight_max
    """
    n = covar.shape[0]
    z = cvx.Variable(n + 1)
    y = z[:n]
    k = z[n]
    objective = cvx.Minimize(cvx.quad_form(y, covar))
    constraints = [means.T @ y == 1.0]
    if is_gross_notional_one:
        constraints = constraints + [cvx.sum(y) == k]
    if is_long_only:
        constraints = constraints + [y >= 0]
    if exposure_budget_eq is not None:
        constraints = constraints + [exposure_budget_eq[0] @ y == exposure_budget_eq[1] * k]
    if exposure_budget_le is not None:
        constraints = constraints + [exposure_budget_le[0] @ y <= exposure_budget_le[1] * k]
    if weight_mins is not None:
        constraints = constraints + [y >= k * weight_mins]
    if weight_maxs is not None:
        constraints = constraints + [y <= k * weight_maxs]
    problem = cvx.Problem(objective, constraints)
    problem.solve()
    optimal_weights = z.value
    if optimal_weights is not None:
        optimal_weights = optimal_weights[:n] / optimal_weights[n]
    else:
        print(f'max_port_sharpe_qp optimal_weights not found = {optimal_weights}')
        print(f'covar={covar}')
        print(f'means={means}')
        if weight_mins is not None:
            print(f'setting optimal_weights to weight_min = {weight_mins}')
            optimal_weights = weight_mins
        else:
            print(f'setting optimal_weights to 0')
            optimal_weights = np.zeros_like(n)
    if is_print_log:
        weights_str = ' '.join([f'{w:0.3f}' for w in optimal_weights])
        print(weights_str)
    return optimal_weights

@jit(nopython=True)
def solve_analytic_log_opt(covar: np.ndarray, means: np.ndarray, exposure_budget_eq: Tuple[np.ndarray, float]=None, gamma: float=1.0) -> np.ndarray:
    """
    analytic solution for max{means^t*w - 0.5*gamma*w^t*covar*w}
    subject to exposure_budget_eq[0]^t*w = exposure_budget_eq[1]
    """
    sigma_i = np.linalg.inv(covar)
    if exposure_budget_eq is not None:
        a = exposure_budget_eq[0]
        a0 = exposure_budget_eq[1]
        a_sigma_a = a.T @ sigma_i @ a
        a_sigma_mu = a.T @ sigma_i @ means
        l_lambda = (-gamma * a0 + a_sigma_mu) / a_sigma_a
        optimal_weights = 1.0 / gamma * sigma_i @ (means - l_lambda * a)
    else:
        optimal_weights = 1.0 / gamma * sigma_i @ means
    return optimal_weights

def print_portfolio_outputs(optimal_weights: np.ndarray, covar: np.ndarray, means: np.ndarray) -> None:
    mean = means.T @ optimal_weights
    vol = np.sqrt(optimal_weights.T @ covar @ optimal_weights)
    sharpe = mean / vol
    inst_sharpes = means / np.sqrt(np.diag(covar))
    sharpe_weighted = inst_sharpes.T @ (optimal_weights / np.sum(optimal_weights))
    line_str = f'expected={mean: 0.2%}, vol={vol: 0.2%}, Sharpe={sharpe: 0.2f}, weighted Sharpe={sharpe_weighted: 0.2f}, inst Sharpes={np.array2string(inst_sharpes, precision=2)}, weights={np.array2string(optimal_weights, precision=2)}'
    print(line_str)

class UnitTests(Enum):
    MIN_VAR = 1
    MAX_UTILITY = 2
    EFFICIENT_FRONTIER = 3
    MAX_UTILITY_VOL_TARGET = 4
    SHARPE = 5
    REGIME_SHARPE = 6

def run_unit_test(unit_test: UnitTests):
    means = np.array([-0.01, 0.05])
    covar = np.array([[0.2 ** 2, -0.0075], [-0.0075, 0.1 ** 2]])
    if unit_test == UnitTests.MIN_VAR:
        weight_min = np.array([0.0, 0.0])
        weight_max = np.array([10.0, 10.0])
        optimal_weights = maximize_portfolio_objective_qp(portfolio_objective=PortfolioObjective.MIN_VAR, covar=covar, means=means, weight_mins=None, weight_maxs=None, is_gross_notional_one=True, is_long_only=True, exposure_budget_eq=None)
        print_portfolio_outputs(optimal_weights=optimal_weights, covar=covar, means=means)
    elif unit_test == UnitTests.MAX_UTILITY:
        gamma = 50 * np.trace(covar)
        optimal_weights = maximize_portfolio_objective_qp(portfolio_objective=PortfolioObjective.MAX_LOG_UTIL, covar=covar, means=means, weight_mins=None, weight_maxs=None, is_gross_notional_one=False, is_long_only=True, exposure_budget_eq=None, gamma=gamma)
        print_portfolio_outputs(optimal_weights=optimal_weights, covar=covar, means=means)
    elif unit_test == UnitTests.EFFICIENT_FRONTIER:
        portfolio_mus = []
        portfolio_vols = []
        portfolio_sharpes = []
        w_lambdas = []
        lang_lambdas = np.arange(0.5, 100.0, 1.0)
        exposure_budget_eq = (np.ones_like(means), 1.0)
        for lang_lambda in lang_lambdas:
            is_analytic = False
            if is_analytic:
                w_lambda = solve_analytic_log_opt(covar=covar, means=means, exposure_budget_eq=exposure_budget_eq, gamma=lang_lambda)
            else:
                w_lambda = maximize_portfolio_objective_qp(portfolio_objective=PortfolioObjective.MAX_LOG_UTIL, covar=covar, means=means, is_gross_notional_one=True, gamma=lang_lambda)
            portfolio_vol = np.sqrt(w_lambda.T @ covar @ w_lambda)
            portfolio_sharpe = means.T @ w_lambda / portfolio_vol
            portfolio_mus.append(means.T @ w_lambda)
            w_lambdas.append(w_lambda)
            portfolio_vols.append(portfolio_vol)
            portfolio_sharpes.append(portfolio_sharpe)
        portfolio_return = pd.Series(portfolio_mus, index=lang_lambdas).rename('mean')
        portfolio_vol = pd.Series(portfolio_vols, index=lang_lambdas).rename('vol')
        portfolio_sharpe = pd.Series(portfolio_sharpes, index=lang_lambdas).rename('Sharpe')
        w_lambdas = pd.DataFrame(w_lambdas, index=lang_lambdas)
        protfolio_data = pd.concat([portfolio_return, portfolio_vol, portfolio_sharpe, w_lambdas], axis=1)
        print(protfolio_data)
        (fig, axs) = plt.subplots(2, 1, figsize=(15, 12))
        sns.lineplot(x='vol', y='mean', data=protfolio_data, ax=axs[0])
        sns.lineplot(data=protfolio_data[['mean', 'vol']], ax=axs[1])
    elif unit_test == UnitTests.MAX_UTILITY_VOL_TARGET:
        optimal_weights = max_qp_portfolio_vol_target(portfolio_objective=PortfolioObjective.MAX_LOG_UTIL, covar=covar, means=means, weight_min=None, weight_max=None, is_gross_notional_one=True, is_long_only=True, exposure_budget_eq=None, vol_target=0.08)
        print_portfolio_outputs(optimal_weights=optimal_weights, covar=covar, means=means)
    elif unit_test == UnitTests.SHARPE:
        portfolio_mus = []
        portfolio_vols = []
        portfolio_sharpes = []
        exposure_budget_eq = (np.ones_like(means), 1.0)
        lang_lambdas = np.arange(1.0, 20.0, 1.0)
        for lang_lambda in lang_lambdas:
            is_analytic = True
            if is_analytic:
                w_lambda = solve_analytic_log_opt(covar=covar, means=means, exposure_budget_eq=exposure_budget_eq, gamma=lang_lambda)
            else:
                w_lambda = maximize_portfolio_objective_qp(portfolio_objective=PortfolioObjective.MAX_LOG_UTIL, covar=covar, means=means, exposure_budget_eq=exposure_budget_eq, gamma=lang_lambda)
            print(f'portfolio with lambda = {lang_lambda}')
            print_portfolio_outputs(optimal_weights=w_lambda, covar=covar, means=means)
            portfolio_vol = np.sqrt(w_lambda.T @ covar @ w_lambda)
            portfolio_sharpe = means.T @ w_lambda / portfolio_vol
            portfolio_mus.append(means.T @ w_lambda)
            portfolio_vols.append(portfolio_vol)
            portfolio_sharpes.append(portfolio_sharpe)
        portfolio_return = pd.Series(portfolio_mus, index=lang_lambdas)
        portfolio_vol = pd.Series(portfolio_vols, index=lang_lambdas)
        portfolio_sharpe = pd.Series(portfolio_sharpes, index=lang_lambdas)
        protfolio_data = pd.concat([portfolio_return, portfolio_vol, portfolio_sharpe], axis=1)
        print(protfolio_data)
        opt_sharpe_w = max_portfolio_sharpe_qp(covar=covar, means=means, exposure_budget_eq=exposure_budget_eq)
        print(f'exact solution')
        print_portfolio_outputs(optimal_weights=opt_sharpe_w, covar=covar, means=means)
    elif unit_test == UnitTests.REGIME_SHARPE:
        g = 3
        sharpes = np.array((0.4, 0.3))
        betas_port = np.array((1.0, 0.8, 1.0))
        betas_cta = np.array((-1.0, 0.25, 0.25))
        idio_vols = np.array((0.01, 0.1))
        p_regimes = np.array((0.16, 0.68, 0.16))
        factor_vol = 0.15
        betas_matrix = np.stack((betas_port, betas_cta))
        print(betas_matrix)
        n = betas_matrix.shape[0]
        covar = np.zeros((n, n))
        for g_ in range(g):
            b = betas_matrix[:, g_]
            covar_regime = np.outer(b, b)
            print(f'covar_regime=\n{covar_regime}')
            covar += covar_regime * p_regimes[g_]
        covar = factor_vol ** 2 * covar + np.diag(idio_vols ** 2)
        print(f't_covar_regime=\n{covar}')
        implied_vols = np.sqrt(np.diag(covar))
        print(f'implied_vols=\n{implied_vols}')
        means = sharpes * implied_vols
        print(f'implied_means=\n{means}')
        exposure_budget_eq = (np.array([1.0, 0.0]), 1.0)
        optimal_weights = max_portfolio_sharpe_qp(covar=covar, means=means, exposure_budget_eq=exposure_budget_eq)
        print_portfolio_outputs(optimal_weights=optimal_weights, covar=covar, means=means)
    plt.show()
if __name__ == '__main__':
    unit_test = UnitTests.SHARPE
    is_run_all_tests = False
    if is_run_all_tests:
        for unit_test in UnitTests:
            run_unit_test(unit_test=unit_test)
    else:
        run_unit_test(unit_test=unit_test)