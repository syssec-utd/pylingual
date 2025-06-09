def get_broadcast_shape(*tensors):
    """Get broadcast shape as a Python list of integers (preferred) or `Tensor`.

  Args:
    *tensors:  One or more `Tensor` objects (already converted!).

  Returns:
    broadcast shape:  Python list (if shapes determined statically), otherwise
      an `int32` `Tensor`.
  """
    s_shape = tensors[0].shape
    for t in tensors[1:]:
        s_shape = tf.broadcast_static_shape(s_shape, t.shape)
    if tensorshape_util.is_fully_defined(s_shape):
        return tensorshape_util.as_list(s_shape)
    d_shape = tf.shape(input=tensors[0])
    for t in tensors[1:]:
        d_shape = tf.broadcast_dynamic_shape(d_shape, tf.shape(input=t))
    return d_shape