def build_kalman_sample_step(get_transition_matrix_for_timestep, get_transition_noise_for_timestep, get_observation_matrix_for_timestep, get_observation_noise_for_timestep, full_sample_and_batch_shape, stream, validate_args=False):
    """Build a callable for one step of Kalman sampling recursion.

  Args:
    get_transition_matrix_for_timestep: callable taking a timestep
      as an integer `Tensor` argument, and returning a `LinearOperator`
      of shape `[latent_size, latent_size]`.
    get_transition_noise_for_timestep: callable taking a timestep as
      an integer `Tensor` argument, and returning a
      `MultivariateNormalLinearOperator` of event shape
      `[latent_size]`.
    get_observation_matrix_for_timestep: callable taking a timestep
      as an integer `Tensor` argument, and returning a `LinearOperator`
      of shape `[observation_size, observation_size]`.
    get_observation_noise_for_timestep: callable taking a timestep as
      an integer `Tensor` argument, and returning a
      `MultivariateNormalLinearOperator` of event shape
      `[observation_size]`.
    full_sample_and_batch_shape: Desired sample and batch shape of the
      returned samples, concatenated in a single `Tensor`.
    stream: `tfd.SeedStream` instance used to generate a
      sequence of random seeds.
    validate_args: if True, perform error checking at runtime.

  Returns:
    sample_step: a callable that samples the latent state and
      observation at time `t`, given latent state at time `t-1`.
  """

    def sample_step(sampled_prev, t):
        """Sample values for a single timestep."""
        latent_prev, _ = sampled_prev
        transition_matrix = get_transition_matrix_for_timestep(t - 1)
        transition_noise = get_transition_noise_for_timestep(t - 1)
        latent_pred = transition_matrix.matmul(latent_prev)
        latent_sampled = latent_pred + transition_noise.sample(sample_shape=_augment_sample_shape(transition_noise, full_sample_and_batch_shape, validate_args), seed=stream())[..., tf.newaxis]
        observation_matrix = get_observation_matrix_for_timestep(t)
        observation_noise = get_observation_noise_for_timestep(t)
        observation_pred = observation_matrix.matmul(latent_sampled)
        observation_sampled = observation_pred + observation_noise.sample(sample_shape=_augment_sample_shape(observation_noise, full_sample_and_batch_shape, validate_args), seed=stream())[..., tf.newaxis]
        return (latent_sampled, observation_sampled)
    return sample_step