import numpy as np
import scipy.stats as sts
EPS = 1e-05

def linear_reg(x: np.ndarray, y: np.ndarray):
    """ Simple linear regression y[idx] = slope[idx] * x + intcp[idx]
    Args:
        x (np.ndarray): shape = (time,)
        y (np.ndarray): shape = (time,*number)
        x's dim0 must equal to y'dim0 !

    Returns:
        slope (np.ndarray): Slope, shape = [*number]
        intcpt (np.ndarray) : intercept , shape = [*number]
        corr (np.ndarray) : Simple correlation coefficient , shape = [*number]
        p_value (np.ndarray) : T test p value , shape = [*number]
    """
    Num0 = x.shape[0]
    Num1 = y.shape[0]
    org_sp_Y = y.shape
    if Num0 != Num1:
        raise ValueError('x.shape[0] no equal to y.shape[0] , dim0 is wrong')
    y_rs = y.reshape(Num1, -1)
    xa = x - x.mean(axis=0)
    ya = y_rs - y_rs.mean(axis=0)
    y_std = ya.std(axis=0)
    x_std = xa.std(axis=0)
    covar = ya.T @ xa / Num0
    corr = covar / y_std / x_std
    slope = corr * y_std / x_std
    intcpt = y_rs.mean(axis=0) - slope * x.mean(axis=0)
    t = corr / (np.sqrt(1 - corr ** 2) + EPS) * np.sqrt(Num0 - 2)
    p_value = sts.t.sf(t, df=Num0 - 2)
    pv_cp = np.copy(p_value)
    p_value[pv_cp >= 0.5] = (1 - p_value[pv_cp >= 0.5]) * 2
    p_value[pv_cp < 0.5] = p_value[pv_cp < 0.5] * 2
    (slope, intcpt, corr, p_value) = list(map(lambda inar: inar.reshape(org_sp_Y[1:]), [slope, intcpt, corr, p_value]))
    return (slope, intcpt, corr, p_value)

def multi_linreg(x: np.ndarray, y: np.ndarray):
    """ multiple linear regression :: y[idx] = slope[idx,0] * x[0] + slope[idx, 1] * x[1] + ... + intcp[idx]

    Args:
        x (np.ndarray): shape = (time, N) ; N is Number of factors
        y (np.ndarray): shape = (time,*number)
        x's dim0 must equal to y'dim0 !
    Returns:
        slope (np.ndarray): Slope, shape = [N,*number]
        intcpt (np.ndarray) : intercept , shape = [*number]
        R (np.ndarray) : multiple correlation coefficient , shape = [*number]
        pv_all(np.ndarray) : F test p value , shape = [*number]
        pv_i(np.ndarray) : F test p value of every infact, shape = [N, *number]
    """
    Num0 = x.shape[0]
    Num1 = y.shape[0]
    Numf = x.shape[1]
    org_sp_Y = y.shape
    if Num0 != Num1:
        raise ValueError('x.shape[0] no equal to y.shape[0] , dim0 is wrong')
    y_rs = y.reshape(Num1, -1)
    x_mean = x.mean(axis=0)
    y_mean = y_rs.mean(axis=0)
    xa = x - x_mean
    ya = y_rs - y_mean
    covar_xx = xa.T @ xa / Num0
    covar_yx = xa.T @ ya / Num0
    slope = np.linalg.solve(covar_xx, covar_yx)
    intcpt = y_mean - slope.T @ x_mean
    y_pre = xa @ slope
    SSyy = Num0 * y_rs.var(axis=0)
    U = Num0 * y_pre.var(axis=0)
    Q = SSyy - U
    R = np.sqrt(U / SSyy)
    F = U / Numf / (Q / (Num0 - Numf - 1))
    C_mx = np.diagonal(np.linalg.inv(covar_xx))
    Q_mx = slope ** 2 / C_mx[..., np.newaxis]
    F_i = Q_mx / (Q / (Num0 - Numf - 1))
    pv_all = 1 - sts.f.cdf(F, Num0 - Numf - 1, Num0)
    pv_i = 1 - sts.f.cdf(F_i, Num0 - Numf - 1, 1)
    (pv_all, R, intcpt) = list(map(lambda inar: inar.reshape(org_sp_Y[1:]), [pv_all, R, intcpt]))
    (slope, pv_i) = list(map(lambda inar: inar.reshape([Numf, *org_sp_Y[1:]]), [slope, pv_i]))
    return (slope, intcpt, R, pv_all, pv_i)