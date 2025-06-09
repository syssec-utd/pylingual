def quadrature_scheme_softmaxnormal_gauss_hermite(normal_loc, normal_scale, quadrature_size, validate_args=False, name=None):
    """Use Gauss-Hermite quadrature to form quadrature on `K - 1` simplex.

  A `SoftmaxNormal` random variable `Y` may be generated via

  ```
  Y = SoftmaxCentered(X),
  X = Normal(normal_loc, normal_scale)
  ```

  Note: for a given `quadrature_size`, this method is generally less accurate
  than `quadrature_scheme_softmaxnormal_quantiles`.

  Args:
    normal_loc: `float`-like `Tensor` with shape `[b1, ..., bB, K-1]`, B>=0.
      The location parameter of the Normal used to construct the SoftmaxNormal.
    normal_scale: `float`-like `Tensor`. Broadcastable with `normal_loc`.
      The scale parameter of the Normal used to construct the SoftmaxNormal.
    quadrature_size: Python `int` scalar representing the number of quadrature
      points.
    validate_args: Python `bool`, default `False`. When `True` distribution
      parameters are checked for validity despite possibly degrading runtime
      performance. When `False` invalid inputs may silently render incorrect
      outputs.
    name: Python `str` name prefixed to Ops created by this class.

  Returns:
    grid: Shape `[b1, ..., bB, K, quadrature_size]` `Tensor` representing the
      convex combination of affine parameters for `K` components.
      `grid[..., :, n]` is the `n`-th grid point, living in the `K - 1` simplex.
    probs:  Shape `[b1, ..., bB, K, quadrature_size]` `Tensor` representing the
      associated with each grid point.
  """
    with tf.name_scope(name or 'quadrature_scheme_softmaxnormal_gauss_hermite'):
        normal_loc = tf.convert_to_tensor(value=normal_loc, name='normal_loc')
        npdt = dtype_util.as_numpy_dtype(normal_loc.dtype)
        normal_scale = tf.convert_to_tensor(value=normal_scale, dtype=npdt, name='normal_scale')
        normal_scale = maybe_check_quadrature_param(normal_scale, 'normal_scale', validate_args)
        grid, probs = np.polynomial.hermite.hermgauss(deg=quadrature_size)
        grid = grid.astype(npdt)
        probs = probs.astype(npdt)
        probs /= np.linalg.norm(probs, ord=1, keepdims=True)
        probs = tf.convert_to_tensor(value=probs, name='probs', dtype=npdt)
        grid = softmax(-distribution_util.pad(normal_loc[..., tf.newaxis] + np.sqrt(2.0) * normal_scale[..., tf.newaxis] * grid, axis=-2, front=True), axis=-2)
        return (grid, probs)