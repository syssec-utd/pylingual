def assert_finite(x, data=None, summarize=None, message=None, name=None):
    """Assert all elements of `x` are finite.

  Args:
    x:  Numeric `Tensor`.
    data:  The tensors to print out if the condition is False.  Defaults to
      error message and first few entries of `x`.
    summarize: Print this many entries of each tensor.
    message: A string to prefix to the default message.
    name: A name for this operation (optional).
      Defaults to "assert_finite".

  Returns:
    Op raising `InvalidArgumentError` unless `x` has specified rank or lower.
    If static checks determine `x` has correct rank, a `no_op` is returned.

  Raises:
    ValueError:  If static checks determine `x` has wrong rank.
  """
    with tf.compat.v2.name_scope(name or 'assert_finite'):
        x_ = tf.get_static_value(x)
        if x_ is not None:
            if ~np.all(np.isfinite(x_)):
                raise ValueError(message)
            return x
        assertion = tf.compat.v1.assert_equal(tf.math.is_finite(x), tf.ones_like(x, tf.bool), data=data, summarize=summarize, message=message)
        with tf.control_dependencies([assertion]):
            return tf.identity(x)