def pick_vector(cond, true_vector, false_vector, name='pick_vector'):
    """Picks possibly different length row `Tensor`s based on condition.

  Value `Tensor`s should have exactly one dimension.

  If `cond` is a python Boolean or `tf.constant` then either `true_vector` or
  `false_vector` is immediately returned. I.e., no graph nodes are created and
  no validation happens.

  Args:
    cond: `Tensor`. Must have `dtype=tf.bool` and be scalar.
    true_vector: `Tensor` of one dimension. Returned when cond is `True`.
    false_vector: `Tensor` of one dimension. Returned when cond is `False`.
    name: Python `str`. The name to give this op.
  Example:  ```python pick_vector(tf.less(0, 5), tf.range(10, 12), tf.range(15,
    18))  # [10, 11] pick_vector(tf.less(5, 0), tf.range(10, 12), tf.range(15,
    18))  # [15, 16, 17] ```

  Returns:
    true_or_false_vector: `Tensor`.

  Raises:
    TypeError: if `cond.dtype != tf.bool`
    TypeError: if `cond` is not a constant and
      `true_vector.dtype != false_vector.dtype`
  """
    with tf.name_scope(name):
        cond = tf.convert_to_tensor(value=cond, dtype_hint=tf.bool, name='cond')
        if cond.dtype != tf.bool:
            raise TypeError('{}.dtype={} which is not {}'.format(cond, cond.dtype, tf.bool))
        true_vector = tf.convert_to_tensor(value=true_vector, name='true_vector')
        false_vector = tf.convert_to_tensor(value=false_vector, name='false_vector')
        if true_vector.dtype != false_vector.dtype:
            raise TypeError('{}.dtype={} does not match {}.dtype={}'.format(true_vector, true_vector.dtype, false_vector, false_vector.dtype))
        cond_value_static = tf.get_static_value(cond)
        if cond_value_static is not None:
            return true_vector if cond_value_static else false_vector
        n = tf.shape(input=true_vector)[0]
        return tf.slice(tf.concat([true_vector, false_vector], 0), [tf.where(cond, 0, n)], [tf.where(cond, n, -1)])