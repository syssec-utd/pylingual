def _prepare_args(objective_function, initial_simplex, initial_vertex, step_sizes, objective_at_initial_simplex, objective_at_initial_vertex, batch_evaluate_objective):
    """Computes the initial simplex and the objective values at the simplex.

  Args:
    objective_function:  A Python callable that accepts a point as a
      real `Tensor` and returns a `Tensor` of real dtype containing
      the value of the function at that point. The function
      to be evaluated at the simplex. If `batch_evaluate_objective` is `True`,
      the callable may be evaluated on a `Tensor` of shape `[n+1] + s `
      where `n` is the dimension of the problem and `s` is the shape of a
      single point in the domain (so `n` is the size of a `Tensor`
      representing a single point).
      In this case, the expected return value is a `Tensor` of shape `[n+1]`.
    initial_simplex: None or `Tensor` of real dtype. The initial simplex to
      start the search. If supplied, should be a `Tensor` of shape `[n+1] + s`
      where `n` is the dimension of the problem and `s` is the shape of a
      single point in the domain. Each row (i.e. the `Tensor` with a given
      value of the first index) is interpreted as a vertex of a simplex and
      hence the rows must be affinely independent. If not supplied, an axes
      aligned simplex is constructed using the `initial_vertex` and
      `step_sizes`. Only one and at least one of `initial_simplex` and
      `initial_vertex` must be supplied.
    initial_vertex: None or `Tensor` of real dtype and any shape that can
      be consumed by the `objective_function`. A single point in the domain that
      will be used to construct an axes aligned initial simplex.
    step_sizes: None or `Tensor` of real dtype and shape broadcasting
      compatible with `initial_vertex`. Supplies the simplex scale along each
      axes. Only used if `initial_simplex` is not supplied. See the docstring
      of `minimize` for more details.
    objective_at_initial_simplex: None or rank `1` `Tensor` of real dtype.
      The value of the objective function at the initial simplex.
      May be supplied only if `initial_simplex` is
      supplied. If not supplied, it will be computed.
    objective_at_initial_vertex: None or scalar `Tensor` of real dtype. The
      value of the objective function at the initial vertex. May be supplied
      only if the `initial_vertex` is also supplied.
    batch_evaluate_objective: Python `bool`. If True, the objective function
      will be evaluated on all the vertices of the simplex packed into a
      single tensor. If False, the objective will be mapped across each
      vertex separately.

  Returns:
    prepared_args: A tuple containing the following elements:
      dimension: Scalar `Tensor` of `int32` dtype. The dimension of the problem
        as inferred from the supplied arguments.
      num_vertices: Scalar `Tensor` of `int32` dtype. The number of vertices
        in the simplex.
      simplex: A `Tensor` of same dtype as `initial_simplex`
        (or `initial_vertex`). The first component of the shape of the
        `Tensor` is `num_vertices` and each element represents a vertex of
        the simplex.
      objective_at_simplex: A `Tensor` of same dtype as the dtype of the
        return value of objective_function. The shape is a vector of size
        `num_vertices`. The objective function evaluated at the simplex.
      num_evaluations: An `int32` scalar `Tensor`. The number of points on
        which the objective function was evaluated.

  Raises:
    ValueError: If any of the following conditions hold
      1. If none or more than one of `initial_simplex` and `initial_vertex` are
        supplied.
      2. If `initial_simplex` and `step_sizes` are both specified.
  """
    if objective_at_initial_simplex is not None and initial_simplex is None:
        raise ValueError('`objective_at_initial_simplex` specified but the`initial_simplex` was not.')
    if objective_at_initial_vertex is not None and initial_vertex is None:
        raise ValueError('`objective_at_initial_vertex` specified but the`initial_vertex` was not.')
    if initial_simplex is not None:
        if initial_vertex is not None:
            raise ValueError('Both `initial_simplex` and `initial_vertex` specified. Only one of the two should be specified.')
        if step_sizes is not None:
            raise ValueError('`step_sizes` must not be specified when an `initial_simplex` has been specified.')
        return _prepare_args_with_initial_simplex(objective_function, initial_simplex, objective_at_initial_simplex, batch_evaluate_objective)
    if initial_vertex is None:
        raise ValueError('One of `initial_simplex` or `initial_vertex` must be supplied')
    if step_sizes is None:
        step_sizes = _default_step_sizes(initial_vertex)
    return _prepare_args_with_initial_vertex(objective_function, initial_vertex, step_sizes, objective_at_initial_vertex, batch_evaluate_objective)