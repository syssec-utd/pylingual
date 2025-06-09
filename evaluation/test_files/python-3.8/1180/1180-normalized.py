def default_mean_field_normal_fn(is_singular=False, loc_initializer=tf.compat.v1.initializers.random_normal(stddev=0.1), untransformed_scale_initializer=tf.compat.v1.initializers.random_normal(mean=-3.0, stddev=0.1), loc_regularizer=None, untransformed_scale_regularizer=None, loc_constraint=None, untransformed_scale_constraint=None):
    """Creates a function to build Normal distributions with trainable params.

  This function produces a closure which produces `tfd.Normal`
  parameterized by a loc` and `scale` each created using `tf.get_variable`.

  Args:
    is_singular: Python `bool` if `True`, forces the special case limit of
      `scale->0`, i.e., a `Deterministic` distribution.
    loc_initializer: Initializer function for the `loc` parameters.
      The default is `tf.random_normal_initializer(mean=0., stddev=0.1)`.
    untransformed_scale_initializer: Initializer function for the `scale`
      parameters. Default value: `tf.random_normal_initializer(mean=-3.,
      stddev=0.1)`. This implies the softplus transformed result is initialized
      near `0`. It allows a `Normal` distribution with `scale` parameter set to
      this value to approximately act like a point mass.
    loc_regularizer: Regularizer function for the `loc` parameters.
    untransformed_scale_regularizer: Regularizer function for the `scale`
      parameters.
    loc_constraint: An optional projection function to be applied to the
      loc after being updated by an `Optimizer`. The function must take as input
      the unprojected variable and must return the projected variable (which
      must have the same shape). Constraints are not safe to use when doing
      asynchronous distributed training.
    untransformed_scale_constraint: An optional projection function to be
      applied to the `scale` parameters after being updated by an `Optimizer`
      (e.g. used to implement norm constraints or value constraints). The
      function must take as input the unprojected variable and must return the
      projected variable (which must have the same shape). Constraints are not
      safe to use when doing asynchronous distributed training.

  Returns:
    make_normal_fn: Python `callable` which creates a `tfd.Normal`
      using from args: `dtype, shape, name, trainable, add_variable_fn`.
  """
    loc_scale_fn = default_loc_scale_fn(is_singular=is_singular, loc_initializer=loc_initializer, untransformed_scale_initializer=untransformed_scale_initializer, loc_regularizer=loc_regularizer, untransformed_scale_regularizer=untransformed_scale_regularizer, loc_constraint=loc_constraint, untransformed_scale_constraint=untransformed_scale_constraint)

    def _fn(dtype, shape, name, trainable, add_variable_fn):
        """Creates multivariate `Deterministic` or `Normal` distribution.

    Args:
      dtype: Type of parameter's event.
      shape: Python `list`-like representing the parameter's event shape.
      name: Python `str` name prepended to any created (or existing)
        `tf.Variable`s.
      trainable: Python `bool` indicating all created `tf.Variable`s should be
        added to the graph collection `GraphKeys.TRAINABLE_VARIABLES`.
      add_variable_fn: `tf.get_variable`-like `callable` used to create (or
        access existing) `tf.Variable`s.

    Returns:
      Multivariate `Deterministic` or `Normal` distribution.
    """
        (loc, scale) = loc_scale_fn(dtype, shape, name, trainable, add_variable_fn)
        if scale is None:
            dist = tfd.Deterministic(loc=loc)
        else:
            dist = tfd.Normal(loc=loc, scale=scale)
        batch_ndims = tf.size(input=dist.batch_shape_tensor())
        return tfd.Independent(dist, reinterpreted_batch_ndims=batch_ndims)
    return _fn