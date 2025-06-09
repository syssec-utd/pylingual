def quadrature_scheme_lognormal_gauss_hermite(loc, scale, quadrature_size, validate_args=False, name=None):
    """Use Gauss-Hermite quadrature to form quadrature on positive-reals.

  Note: for a given `quadrature_size`, this method is generally less accurate
  than `quadrature_scheme_lognormal_quantiles`.

  Args:
    loc: `float`-like (batch of) scalar `Tensor`; the location parameter of
      the LogNormal prior.
    scale: `float`-like (batch of) scalar `Tensor`; the scale parameter of
      the LogNormal prior.
    quadrature_size: Python `int` scalar representing the number of quadrature
      points.
    validate_args: Python `bool`, default `False`. When `True` distribution
      parameters are checked for validity despite possibly degrading runtime
      performance. When `False` invalid inputs may silently render incorrect
      outputs.
    name: Python `str` name prefixed to Ops created by this class.

  Returns:
    grid: (Batch of) length-`quadrature_size` vectors representing the
      `log_rate` parameters of a `Poisson`.
    probs: (Batch of) length-`quadrature_size` vectors representing the
      weight associate with each `grid` value.
  """
    with tf.name_scope(name or 'vector_diffeomixture_quadrature_gauss_hermite'):
        (grid, probs) = np.polynomial.hermite.hermgauss(deg=quadrature_size)
        npdt = dtype_util.as_numpy_dtype(loc.dtype)
        grid = grid.astype(npdt)
        probs = probs.astype(npdt)
        probs /= np.linalg.norm(probs, ord=1, keepdims=True)
        probs = tf.convert_to_tensor(value=probs, name='probs', dtype=loc.dtype)
        grid = loc[..., tf.newaxis] + np.sqrt(2.0) * scale[..., tf.newaxis] * grid
        return (grid, probs)