def _get_starting_population(initial_population, initial_position, population_size, population_stddev, seed):
    """Constructs the initial population.

  If an initial population is not already provided, this function constructs
  a population by adding random normal noise to the initial position.

  Args:
    initial_population: None or a list of `Tensor`s. The initial population.
    initial_position: None or a list of `Tensor`s. The initial position.
      If initial_population is None, this argument must not be None.
    population_size: Scalar integer `Tensor`. The number of members in the
      population. If the initial population is not None, this parameter is
      ignored.
    population_stddev: A positive scalar real `Tensor` of the same dtype
      as `initial_position` or `initial_population` (whichever is not None).
      This parameter is ignored if `initial_population`
      is specified. Used to generate the population from the
      `initial_position` by adding random normal noise with zero mean and
      the specified standard deviation.
    seed: Seed for random number generation.

  Returns:
    A list of `Tensor`s. The initial population.
  """
    if initial_population is not None:
        return [tf.convert_to_tensor(value=part) for part in initial_population]
    seed_stream = distributions.SeedStream(seed, salt='get_starting_population')
    population = []
    for part in initial_position:
        part = tf.convert_to_tensor(value=part)
        part_event_shape = tf.shape(input=part)
        population_part_shape = tf.concat([[population_size - 1], part_event_shape], axis=0)
        population_part = tf.random.normal(population_part_shape, stddev=population_stddev, dtype=part.dtype.base_dtype, seed=seed_stream())
        population_part += part
        population_part = tf.concat([[part], population_part], axis=0)
        population.append(population_part)
    return population