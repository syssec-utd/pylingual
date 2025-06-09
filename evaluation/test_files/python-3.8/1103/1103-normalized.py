def log_cdf_laplace(x, name='log_cdf_laplace'):
    """Log Laplace distribution function.

  This function calculates `Log[L(x)]`, where `L(x)` is the cumulative
  distribution function of the Laplace distribution, i.e.

  ```L(x) := 0.5 * int_{-infty}^x e^{-|t|} dt```

  For numerical accuracy, `L(x)` is computed in different ways depending on `x`,

  ```
  x <= 0:
    Log[L(x)] = Log[0.5] + x, which is exact

  0 < x:
    Log[L(x)] = Log[1 - 0.5 * e^{-x}], which is exact
  ```

  Args:
    x: `Tensor` of type `float32`, `float64`.
    name: Python string. A name for the operation (default="log_ndtr").

  Returns:
    `Tensor` with `dtype=x.dtype`.

  Raises:
    TypeError: if `x.dtype` is not handled.
  """
    with tf.name_scope(name):
        x = tf.convert_to_tensor(value=x, name='x')
        lower_solution = -np.log(2.0) + x
        safe_exp_neg_x = tf.exp(-tf.abs(x))
        upper_solution = tf.math.log1p(-0.5 * safe_exp_neg_x)
        return tf.where(x < 0.0, lower_solution, upper_solution)