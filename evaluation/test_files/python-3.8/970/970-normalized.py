def random_walk_uniform_fn(scale=1.0, name=None):
    """Returns a callable that adds a random uniform perturbation to the input.

  For more details on `random_walk_uniform_fn`, see
  `random_walk_normal_fn`. `scale` might
  be a `Tensor` or a list of `Tensor`s that should broadcast with state parts
  of the `current_state`. The generated uniform perturbation is sampled as a
  uniform point on the rectangle `[-scale, scale]`.

  Args:
    scale: a `Tensor` or Python `list` of `Tensor`s of any shapes and `dtypes`
      controlling the upper and lower bound of the uniform proposal
      distribution.
    name: Python `str` name prefixed to Ops created by this function.
        Default value: 'random_walk_uniform_fn'.

  Returns:
    random_walk_uniform_fn: A callable accepting a Python `list` of `Tensor`s
      representing the state parts of the `current_state` and an `int`
      representing the random seed used to generate the proposal. The callable
      returns the same-type `list` of `Tensor`s as the input and represents the
      proposal for the RWM algorithm.
  """

    def _fn(state_parts, seed):
        """Adds a uniform perturbation to the input state.

    Args:
      state_parts: A list of `Tensor`s of any shape and real dtype representing
        the state parts of the `current_state` of the Markov chain.
      seed: `int` or None. The random seed for this `Op`. If `None`, no seed is
        applied.
        Default value: `None`.

    Returns:
      perturbed_state_parts: A Python `list` of The `Tensor`s. Has the same
        shape and type as the `state_parts`.

    Raises:
      ValueError: if `scale` does not broadcast with `state_parts`.
    """
        with tf.compat.v1.name_scope(name, 'random_walk_uniform_fn', values=[state_parts, scale, seed]):
            scales = scale if mcmc_util.is_list_like(scale) else [scale]
            if len(scales) == 1:
                scales *= len(state_parts)
            if len(state_parts) != len(scales):
                raise ValueError('`scale` must broadcast with `state_parts`.')
            seed_stream = distributions.SeedStream(seed, salt='RandomWalkUniformFn')
            next_state_parts = [tf.random.uniform(minval=state_part - scale_part, maxval=state_part + scale_part, shape=tf.shape(input=state_part), dtype=state_part.dtype.base_dtype, seed=seed_stream()) for (scale_part, state_part) in zip(scales, state_parts)]
            return next_state_parts
    return _fn