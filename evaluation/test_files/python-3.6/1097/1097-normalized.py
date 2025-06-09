def ndtri(p, name='ndtri'):
    """The inverse of the CDF of the Normal distribution function.

  Returns x such that the area under the pdf from minus infinity to x is equal
  to p.

  A piece-wise rational approximation is done for the function.
  This is a port of the implementation in netlib.

  Args:
    p: `Tensor` of type `float32`, `float64`.
    name: Python string. A name for the operation (default="ndtri").

  Returns:
    x: `Tensor` with `dtype=p.dtype`.

  Raises:
    TypeError: if `p` is not floating-type.
  """
    with tf.name_scope(name):
        p = tf.convert_to_tensor(value=p, name='p')
        if dtype_util.as_numpy_dtype(p.dtype) not in [np.float32, np.float64]:
            raise TypeError('p.dtype=%s is not handled, see docstring for supported types.' % p.dtype)
        return _ndtri(p)