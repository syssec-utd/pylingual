def expand_to_vector(x, tensor_name=None, op_name=None, validate_args=False):
    """Transform a 0-D or 1-D `Tensor` to be 1-D.

  For user convenience, many parts of the TensorFlow Probability API accept
  inputs of rank 0 or 1 -- i.e., allowing an `event_shape` of `[5]` to be passed
  to the API as either `5` or `[5]`.  This function can be used to transform
  such an argument to always be 1-D.

  NOTE: Python or NumPy values will be converted to `Tensor`s with standard type
  inference/conversion.  In particular, an empty list or tuple will become an
  empty `Tensor` with dtype `float32`.  Callers should convert values to
  `Tensor`s before calling this function if different behavior is desired
  (e.g. converting empty lists / other values to `Tensor`s with dtype `int32`).

  Args:
    x: A 0-D or 1-D `Tensor`.
    tensor_name: Python `str` name for `Tensor`s created by this function.
    op_name: Python `str` name for `Op`s created by this function.
    validate_args: Python `bool, default `False`.  When `True`, arguments may be
      checked for validity at execution time, possibly degrading runtime
      performance.  When `False`, invalid inputs may silently render incorrect
        outputs.
  Returns:
    vector: a 1-D `Tensor`.
  """
    with tf.name_scope(op_name or 'expand_to_vector'):
        x = tf.convert_to_tensor(value=x, name='x')
        ndims = tensorshape_util.rank(x.shape)
        if ndims is None:
            if validate_args:
                x = with_dependencies([assert_util.assert_rank_at_most(x, 1, message='Input is neither scalar nor vector.')], x)
            ndims = tf.rank(x)
            expanded_shape = pick_vector(tf.equal(ndims, 0), np.array([1], dtype=np.int32), tf.shape(input=x))
            return tf.reshape(x, expanded_shape)
        elif ndims == 0:
            x_const = tf.get_static_value(x)
            if x_const is not None:
                return tf.convert_to_tensor(value=dtype_util.as_numpy_dtype(x.dtype)([x_const]), name=tensor_name)
            else:
                return tf.reshape(x, [1])
        elif ndims != 1:
            raise ValueError('Input is neither scalar nor vector.')
        return x