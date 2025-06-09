def f_supports(self, data):
    """Sparse matrices support Scipy csr, csc, bsr and dia matrices and everything their parent
        class the :class:`~pypet.parameter.ArrayParameter` supports.

        """
    if self._is_supported_matrix(data):
        return True
    else:
        return super(SparseParameter, self).f_supports(data)