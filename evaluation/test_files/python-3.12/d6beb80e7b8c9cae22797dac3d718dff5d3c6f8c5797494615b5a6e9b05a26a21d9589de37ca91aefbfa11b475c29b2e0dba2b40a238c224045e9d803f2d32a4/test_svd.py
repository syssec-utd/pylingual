"""Tests for SVD functionality."""
from matfree import decomp, test_util
from matfree.backend import linalg, np, testing

@testing.fixture()
@testing.parametrize('nrows', [10])
@testing.parametrize('ncols', [3])
@testing.parametrize('num_significant_singular_vals', [3])
def A(nrows, ncols, num_significant_singular_vals):
    """Make a positive definite matrix with certain spectrum."""
    n = min(nrows, ncols)
    d = np.arange(n) + 10.0
    d = d.at[num_significant_singular_vals:].set(0.001)
    return test_util.asymmetric_matrix_from_singular_values(d, nrows=nrows, ncols=ncols)

def test_equal_to_linalg_svd(A):
    """The output of full-depth SVD should be equal (*) to linalg.svd().

    (*) Note: The singular values should be identical,
    and the orthogonal matrices should be orthogonal. They are not unique.
    """
    nrows, ncols = np.shape(A)
    depth = min(nrows, ncols) - 1

    def Av(v):
        return A @ v

    def vA(v):
        return v @ A
    v0 = np.ones((ncols,))
    U, S, Vt = decomp.svd(v0, depth, Av, vA, matrix_shape=np.shape(A))
    U_, S_, Vt_ = linalg.svd(A, full_matrices=False)
    tols_decomp = {'atol': 1e-05, 'rtol': 1e-05}
    assert np.allclose(S, S_)
    assert np.shape(U) == np.shape(U_)
    assert np.shape(Vt) == np.shape(Vt_)
    assert np.allclose(U @ U.T, U_ @ U_.T, **tols_decomp)
    assert np.allclose(Vt @ Vt.T, Vt_ @ Vt_.T, **tols_decomp)