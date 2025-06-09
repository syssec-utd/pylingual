"""Permute the dimensions of an array."""
from __future__ import annotations
from typing import Sequence, Union
import numpy
import numpoly
from ..baseclass import ndpoly, PolyLike
from ..dispatch import implements

@implements(numpy.transpose)
def transpose(a: PolyLike, axes: Union[None, Sequence[int], numpy.ndarray]=None) -> ndpoly:
    """
    Permute the dimensions of an array.

    Args:
        a:
            Input array.
        axes:
            By default, reverse the dimensions, otherwise permute the axes
            according to the values given.

    Return:
        `a` with its axes permuted. A view is returned whenever possible.

    Example:
        >>> poly = numpoly.monomial([3, 3]).reshape(2, 3)
        >>> poly
        polynomial([[1, q0, q0**2],
                    [q1, q0*q1, q1**2]])
        >>> numpoly.transpose(poly)
        polynomial([[1, q1],
                    [q0, q0*q1],
                    [q0**2, q1**2]])

    """
    a = numpoly.aspolynomial(a)
    out = numpy.transpose(a.values, axes=axes)
    out = numpoly.polynomial(out, names=a.indeterminants)
    return out