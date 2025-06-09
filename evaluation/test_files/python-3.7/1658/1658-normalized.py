def from_ndarray(cls, a_ndarray, bigdl_type='float'):
    """
        Convert a ndarray to a DenseTensor which would be used in Java side.

        >>> import numpy as np
        >>> from bigdl.util.common import JTensor
        >>> from bigdl.util.common import callBigDlFunc
        >>> np.random.seed(123)
        >>> data = np.random.uniform(0, 1, (2, 3)).astype("float32")
        >>> result = JTensor.from_ndarray(data)
        >>> expected_storage = np.array([[0.69646919, 0.28613934, 0.22685145], [0.55131477, 0.71946895, 0.42310646]])
        >>> expected_shape = np.array([2, 3])
        >>> np.testing.assert_allclose(result.storage, expected_storage, rtol=1e-6, atol=1e-6)
        >>> np.testing.assert_allclose(result.shape, expected_shape)
        >>> data_back = result.to_ndarray()
        >>> (data == data_back).all()
        True
        >>> tensor1 = callBigDlFunc("float", "testTensor", JTensor.from_ndarray(data))  # noqa
        >>> array_from_tensor = tensor1.to_ndarray()
        >>> (array_from_tensor == data).all()
        True
        """
    if a_ndarray is None:
        return None
    assert isinstance(a_ndarray, np.ndarray), 'input should be a np.ndarray, not %s' % type(a_ndarray)
    return cls(a_ndarray, a_ndarray.shape if a_ndarray.shape else a_ndarray.size, bigdl_type)