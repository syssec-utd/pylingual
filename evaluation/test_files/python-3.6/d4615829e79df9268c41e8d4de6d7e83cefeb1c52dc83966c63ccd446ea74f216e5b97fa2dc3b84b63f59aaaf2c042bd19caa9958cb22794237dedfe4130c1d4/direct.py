"""
Direct method for piecewise regression with l2-norm objective and no other
constraints.
"""
import numpy as np
from .matrices import submatrix_A

def lsq_direct(x, y, splits, degree):
    order = degree + 1
    n = len(x)
    n_splits = len(splits)
    n_bins = n_splits + 1
    nA = n_bins * order
    A = np.zeros((n, nA))
    S = np.zeros((n_splits, nA))
    indices = np.searchsorted(splits, x, side='right')
    cn = 0
    for i in range(n_bins):
        xi = x[indices == i]
        ni = len(xi)
        pxi = np.ones(ni)
        for j in range(order * i, order * (i + 1)):
            A[cn:cn + ni, j] = pxi
            pxi *= xi
        cn += ni
    exporder = np.arange(order)
    for (i, s) in enumerate(splits):
        r = np.power(s, exporder)
        S[i, order * i:order * (i + 1)] = r
        S[i, order * (i + 1):order * (i + 2)] = -r
    nM = nA + n_splits
    M = np.zeros((nM, nM))
    M[:nA, :nA] = 2 * A.T.dot(A)
    M[:nA, nA:] = S.T
    M[nA:, :nA] = S
    d = np.zeros(nM)
    d[:nA] = 2 * A.T.dot(y)
    c = np.linalg.solve(M, d)
    info = {'status': 'optimal', 'stats': {'n_variables': nA, 'n_constraints': nM}}
    return (c[:nA].reshape((n_bins, order)), info)

def lsq_direct_separated(x, y, splits, degree):
    order = degree + 1
    n_bins = len(splits) + 1
    indices = np.searchsorted(splits, x, side='right')
    c = np.zeros((n_bins, order))
    infos = []
    for i in range(n_bins):
        mask = indices == i
        xi = x[mask]
        yi = y[mask]
        ni = len(xi)
        Ai = submatrix_A(ni, xi, order)
        (ci, _, _, _) = np.linalg.lstsq(Ai, yi, rcond=None)
        info = {'status': 'optimal', 'stats': {'n_variables': order, 'n_constraints': 0}}
        infos.append(info)
        c[i, :] = ci
    return (c, infos)