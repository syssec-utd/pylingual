import pytest
import numpy as np
import awkward as ak

def test():
    array = ak.Array([[1, 2, 3]])
    assert ak.unflatten(array, [2, 1], axis=1).tolist() == [[[1, 2], [3]]]
    assert ak.unflatten(array, [0, 2, 1], axis=1).tolist() == [[[], [1, 2], [3]]]
    assert ak.unflatten(array, [0, 0, 2, 1], axis=1).tolist() == [[[], [], [1, 2], [3]]]