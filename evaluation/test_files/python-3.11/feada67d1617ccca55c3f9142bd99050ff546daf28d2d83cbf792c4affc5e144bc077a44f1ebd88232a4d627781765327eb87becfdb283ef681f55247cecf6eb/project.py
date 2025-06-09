"""
This module provides functions for working with convex hulls and projections.

It provides methods for:

- Projecting a set of vectors until it defines a convex hull.
- Finding the intersection of a line (defined by two vectors) with a simplex.
- Generating combinations of points that result in the projection of a convex hull onto a simplex.
- Projecting the points of a convex hull onto a simplex.
- Projecting a set of arbitrary vectors onto a convex hull defined by hyperplane equations of the facets.
- Finding the multiple of a vector that intersects with the hull.
- Finding the hull intersection of vectors.

Each function includes checks to ensure the integrity of the input and functionality of the methods.
The module utilizes libraries such as numpy, scipy, sklearn, and quadprog to perform complex mathematical operations.
"""
from typing import Tuple, Union, Iterator
from quadprog import solve_qp
from scipy.spatial import ConvexHull, Delaunay
try:
    from scipy.spatial import QhullError
except ImportError:
    from scipy.spatial.qhull import QhullError
from sklearn.decomposition import PCA
import numpy as np
from itertools import product

def proj_P_for_hull(P: np.ndarray, hull_class: Union[ConvexHull, Delaunay]=ConvexHull, return_ndim: bool=False, return_hull: bool=True, return_transformer: bool=False) -> Union[ConvexHull, int, PCA, Tuple[ConvexHull, int], Tuple[ConvexHull, PCA], Tuple[ConvexHull, int, PCA]]:
    """
    This function projects the input array `P` until it defines a convex hull.

    Parameters
    ----------
    P : np.ndarray
        The input array to be projected.
    hull_class : Union[ConvexHull, Delaunay], optional
        The convex hull class to use. Default is ConvexHull.
    return_ndim : bool, optional
        If True, the function returns the number of dimensions. Default is False.
    return_hull : bool, optional
        If True, the function returns the convex hull object. Default is True.
    return_transformer : bool, optional
        If True, the function returns the dimensionality reduction transformer. Default is False.

    Returns
    -------
    ConvexHull or int or PCA or Tuple[ConvexHull, int] or Tuple[ConvexHull, PCA] or Tuple[ConvexHull, int, PCA]
        Depending on the values of `return_ndim`, `return_hull`, and `return_transformer`,
        the function will return the convex hull object,
        the number of dimensions, the dimensionality reduction transformer,
        or some combination of these.

    Raises
    ------
    QhullError
        If QhullError is encountered during the creation of the convex hull.
    """
    try:
        if P.shape[-1] == 1:
            hull = P
            ndim = 1
        else:
            hull = hull_class(P)
            ndim = P.shape[-1]
        svd = None
    except QhullError:
        svd = PCA(P.shape[1] - 1)
        P = svd.fit_transform(P)
        evar = np.cumsum(svd.explained_variance_ratio_)
        ndim = np.min(np.flatnonzero(np.isclose(evar, 1))) + 1
        if ndim == 1:
            hull = P[:, :ndim]
        else:
            hull = hull_class(P[:, :ndim])
    return _get_return_values(return_hull, return_ndim, return_transformer, hull, ndim, svd)

def _get_return_values(return_hull: bool, return_ndim: bool, return_transformer: bool, hull: ConvexHull, ndim: int, svd: PCA) -> Union[ConvexHull, int, PCA, Tuple[ConvexHull, int], Tuple[ConvexHull, PCA], Tuple[ConvexHull, int, PCA]]:
    """
    Helper function to determine the return values based on boolean input flags.

    Parameters
    ----------
    return_hull : bool
        If True, the function includes the convex hull object in the return value.
    return_ndim : bool
        If True, the function includes the number of dimensions in the return value.
    return_transformer : bool
        If True, the function includes the dimensionality reduction transformer in the return value.
    hull : ConvexHull
        The convex hull object.
    ndim : int
        The number of dimensions.
    svd : PCA
        The dimensionality reduction transformer.

    Returns
    -------
    ConvexHull or int or PCA or Tuple[ConvexHull, int] or Tuple[ConvexHull, PCA] or Tuple[ConvexHull, int, PCA]
        Depending on the values of `return_ndim`, `return_hull`, and `return_transformer`,
        the function will return the convex hull object,
        the number of dimensions, the dimensionality reduction transformer,
        or some combination of these.
    """
    if return_hull and (not return_ndim) and (not return_transformer):
        return hull
    elif return_hull and return_ndim and return_transformer:
        return (hull, ndim, svd)
    elif return_hull and return_ndim:
        return (hull, ndim)
    elif return_hull and return_transformer:
        return (hull, svd)
    elif return_transformer:
        return svd
    else:
        return ndim

def line_to_simplex(x1: np.ndarray, x2: np.ndarray, c: float, axis: int=-1, checks: bool=True) -> np.ndarray:
    """
    This function finds the point where the line defined by vectors `x1`
    and `x2` intersects with the simplex with sum of `c`.

    Parameters
    ----------
    x1 : np.ndarray
        The first point defining the line.
    x2 : np.ndarray
        The second point defining the line.
    c : float
        The sum of the simplex.
    axis : int, optional
        The axis to sum over. Default is -1.
    checks : bool, optional
        If True, the function checks the validity of inputs. Default is True.

    Returns
    -------
    np.ndarray
        The intersection point.
    """
    if checks:
        assert np.all(c > 0)
        assert np.all(x1 >= 0)
        assert np.all(x2 >= 0)
    t = (c - np.sum(x1, axis=axis, keepdims=True)) / np.sum(x2 - x1, axis=axis, keepdims=True)
    return x1 + t * (x2 - x1)

def yieldPpairs4proj2simplex(P: np.ndarray, c: float) -> Iterator[Tuple[np.ndarray, np.ndarray]]:
    """
    Yield the combination of points in `P`
    that are between the simplex with sum of `c`
    and whose intersection with the simplex
    would result in the projection of the
    convex hull described by `P` onto the simplex.

    Parameters
    ----------
    P : np.ndarray
        The array of vectors.
    c : float
        Sum of the simplex.

    Yields
    ------
    Tuple[np.ndarray, np.ndarray]
        Combination of points in `P` that are between the simplex.

    Raises
    ------
    AssertionError
        If the target `c` is too low or too high.
    """
    psum = np.sum(P, axis=-1)
    threshbool = psum <= c
    assert np.any(threshbool), 'Target `c` too low.'
    assert not np.all(threshbool), 'Target `c` too high.'
    if P.shape[0] > P.shape[1]:
        hull, ndim = proj_P_for_hull(P, return_ndim=True)
        if ndim == 1:
            p1 = P[threshbool][:1]
            p2 = P[~threshbool][-1:]
            yield from product(p1, p2)
        else:
            idcs1 = np.flatnonzero(threshbool)
            idcs2 = np.flatnonzero(~threshbool)
            edges = []
            for e in hull.simplices:
                for idx, jdx in product(e, e):
                    if idx == jdx:
                        continue
                    if (idx, jdx) in edges or (jdx, idx) in edges:
                        continue
                    if idx in idcs1 and jdx in idcs1:
                        continue
                    if idx in idcs2 and jdx in idcs2:
                        continue
                    if psum[idx] > psum[jdx]:
                        continue
                    edges.append((idx, jdx))
                    yield (P[idx], P[jdx])
    else:
        p1 = P[threshbool]
        p2 = P[~threshbool]
        yield from product(p1, p2)

def proj_P_to_simplex(P: np.ndarray, c: float) -> np.ndarray:
    """
    Project the points that project the convex hull entailed
    by `P` onto the simplex with sum of `c`.
    Each returned point should sum up to `c`.

    Parameters
    ----------
    P : np.ndarray
        The array of points.
    c : float
        The sum of the simplex.

    Returns
    -------
    np.ndarray
        The projected points.

    Raises
    ------
    AssertionError
        If any point in `P` is not positive or `c` is not positive.
    """
    assert np.all(P >= 0), 'All `points` must be positive'
    assert np.all(c > 0), '`c` must be positive'
    return np.array([line_to_simplex(x1, x2, c, checks=False) for x1, x2 in yieldPpairs4proj2simplex(P, c)])

def proj_B_to_hull(B: np.ndarray, equations: np.ndarray) -> np.ndarray:
    """
    Project `B` to the convex hull defined by the
    hyperplane equations of the facets.

    Parameters
    ----------
    B : np.ndarray
        The array of points to be projected.
    equations : np.ndarray
        The hyperplane equations of the facets.

    Returns
    -------
    np.ndarray
        The projected points.
    """
    B = B.astype(np.float64)
    equations = equations.astype(np.float64)
    Q = np.eye(B.shape[-1])
    return np.apply_along_axis(lambda a: solve_qp(Q, a, -equations[:, :-1].T, equations[:, -1], meq=0, factorized=True)[0], -1, B)

def alpha_for_B_with_P(B: np.ndarray, equations: np.ndarray) -> np.ndarray:
    """
    Get the multiple of vector that intersects with the hull.

    Parameters
    ----------
    B : np.ndarray
        The array of vectors.
    equations : np.ndarray
        The hyperplane equations of the facets.

    Returns
    -------
    np.ndarray
        The array of multiples for each vector in `B`.
    """
    equations = equations.T
    V, b = (equations[:-1], equations[-1])
    alpha = -b / (B @ V)
    alpha[alpha <= 0] = np.nan
    return np.nanmin(alpha, axis=-1)

def B_with_P(B: np.ndarray, equations: np.ndarray) -> np.ndarray:
    """
    Find the hull intersection of vectors `B`.

    Parameters
    ----------
    B : np.ndarray
        The array of vectors.
    equations : np.ndarray
        The hyperplane equations of the facets.

    Returns
    -------
    np.ndarray
        The array of intersection points for each vector in `B`.
    """
    return alpha_for_B_with_P(B, equations)[..., None] * B