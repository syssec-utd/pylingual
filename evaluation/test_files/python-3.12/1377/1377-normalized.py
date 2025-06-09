def forward_filter(self, x, mask=None):
    """Run a Kalman filter over a provided sequence of outputs.

    Note that the returned values `filtered_means`, `predicted_means`, and
    `observation_means` depend on the observed time series `x`, while the
    corresponding covariances are independent of the observed series; i.e., they
    depend only on the model itself. This means that the mean values have shape
    `concat([sample_shape(x), batch_shape, [num_timesteps,
    {latent/observation}_size]])`, while the covariances have shape
    `concat[(batch_shape, [num_timesteps, {latent/observation}_size,
    {latent/observation}_size]])`, which does not depend on the sample shape.

    Args:
      x: a float-type `Tensor` with rightmost dimensions
        `[num_timesteps, observation_size]` matching
        `self.event_shape`. Additional dimensions must match or be
        broadcastable to `self.batch_shape`; any further dimensions
        are interpreted as a sample shape.
      mask: optional bool-type `Tensor` with rightmost dimension
        `[num_timesteps]`; `True` values specify that the value of `x`
        at that timestep is masked, i.e., not conditioned on. Additional
        dimensions must match or be broadcastable to `self.batch_shape`; any
        further dimensions must match or be broadcastable to the sample
        shape of `x`.
        Default value: `None`.

    Returns:
      log_likelihoods: Per-timestep log marginal likelihoods `log
        p(x_t | x_{:t-1})` evaluated at the input `x`, as a `Tensor`
        of shape `sample_shape(x) + batch_shape + [num_timesteps].`
      filtered_means: Means of the per-timestep filtered marginal
         distributions p(z_t | x_{:t}), as a Tensor of shape
        `sample_shape(x) + batch_shape + [num_timesteps, latent_size]`.
      filtered_covs: Covariances of the per-timestep filtered marginal
         distributions p(z_t | x_{:t}), as a Tensor of shape
        `sample_shape(mask) + batch_shape + [num_timesteps, latent_size,
        latent_size]`. Note that the covariances depend only on the model and
        the mask, not on the data, so this may have fewer dimensions than
        `filtered_means`.
      predicted_means: Means of the per-timestep predictive
         distributions over latent states, p(z_{t+1} | x_{:t}), as a
         Tensor of shape `sample_shape(x) + batch_shape +
         [num_timesteps, latent_size]`.
      predicted_covs: Covariances of the per-timestep predictive
         distributions over latent states, p(z_{t+1} | x_{:t}), as a
         Tensor of shape `sample_shape(mask) + batch_shape +
         [num_timesteps, latent_size, latent_size]`. Note that the covariances
         depend only on the model and the mask, not on the data, so this may
         have fewer dimensions than `predicted_means`.
      observation_means: Means of the per-timestep predictive
         distributions over observations, p(x_{t} | x_{:t-1}), as a
         Tensor of shape `sample_shape(x) + batch_shape +
         [num_timesteps, observation_size]`.
      observation_covs: Covariances of the per-timestep predictive
         distributions over observations, p(x_{t} | x_{:t-1}), as a
         Tensor of shape `sample_shape(mask) + batch_shape + [num_timesteps,
         observation_size, observation_size]`. Note that the covariances depend
         only on the model and the mask, not on the data, so this may have fewer
         dimensions than `observation_means`.
    """
    with tf.name_scope('forward_filter'):
        x = tf.convert_to_tensor(value=x, name='x')
        if mask is not None:
            mask = tf.convert_to_tensor(value=mask, name='mask', dtype_hint=tf.bool)
        check_x_shape_op = _check_equal_shape('x', x.shape[-2:], tf.shape(input=x)[-2:], self.event_shape, self.event_shape_tensor())
        check_mask_dims_op = None
        check_mask_shape_op = None
        if mask is not None:
            if tensorshape_util.rank(mask.shape) is None or tensorshape_util.rank(x.shape) is None:
                check_mask_dims_op = assert_util.assert_greater_equal(tf.rank(x), tf.rank(mask), message='mask cannot have higher rank than x!')
            elif tensorshape_util.rank(mask.shape) > tensorshape_util.rank(x.shape):
                raise ValueError('mask cannot have higher rank than x! ({} vs {})'.format(tensorshape_util.rank(mask.shape), tensorshape_util.rank(x.shape)))
            check_mask_shape_op = _check_equal_shape('mask', mask.shape[-1:], tf.shape(input=mask)[-1:], self.event_shape[-2:-1], self.event_shape_tensor()[-2:-1])
        if self.validate_args:
            runtime_assertions = self.runtime_assertions
            if check_x_shape_op is not None:
                runtime_assertions += [check_x_shape_op]
            if check_mask_shape_op is not None:
                runtime_assertions += [check_mask_shape_op]
            if check_mask_dims_op is not None:
                runtime_assertions += [check_mask_dims_op]
            with tf.control_dependencies(runtime_assertions):
                x = tf.identity(x)
        if tensorshape_util.is_fully_defined(self.batch_shape) and tensorshape_util.is_fully_defined(x.shape):
            sample_and_batch_shape = tf.broadcast_static_shape(x.shape[:-2], self.batch_shape)
        else:
            sample_and_batch_shape = tf.broadcast_dynamic_shape(tf.shape(input=x)[:-2], self.batch_shape_tensor())
        if mask is None:
            mask_sample_and_batch_shape = self.batch_shape_tensor()
        elif tensorshape_util.is_fully_defined(self.batch_shape) and tensorshape_util.is_fully_defined(mask.shape):
            mask_sample_and_batch_shape = tf.broadcast_static_shape(mask.shape[:-1], self.batch_shape)
        else:
            mask_sample_and_batch_shape = tf.broadcast_dynamic_shape(tf.shape(input=mask)[:-1], self.batch_shape_tensor())
        x = distribution_util.move_dimension(x, -2, 0)
        if mask is not None:
            mask = distribution_util.move_dimension(mask, -1, 0)
        x = x[..., tf.newaxis]
        if mask is not None:
            mask = mask[..., tf.newaxis, tf.newaxis]
        prior_mean = _broadcast_to_shape(self.initial_state_prior.mean()[..., tf.newaxis], tf.concat([sample_and_batch_shape, [self.latent_size, 1]], axis=0))
        prior_cov = _broadcast_to_shape(self.initial_state_prior.covariance(), tf.concat([mask_sample_and_batch_shape, [self.latent_size, self.latent_size]], axis=0))
        initial_observation_matrix = self.get_observation_matrix_for_timestep(self.initial_step)
        initial_observation_noise = self.get_observation_noise_for_timestep(self.initial_step)
        initial_observation_mean = _propagate_mean(prior_mean, initial_observation_matrix, initial_observation_noise)
        initial_observation_cov = _propagate_cov(prior_cov, initial_observation_matrix, initial_observation_noise)
        initial_state = KalmanFilterState(predicted_mean=prior_mean, predicted_cov=prior_cov, filtered_mean=prior_mean, filtered_cov=prior_cov, observation_mean=initial_observation_mean, observation_cov=initial_observation_cov, log_marginal_likelihood=tf.zeros(shape=sample_and_batch_shape, dtype=self.dtype), timestep=tf.convert_to_tensor(value=self.initial_step, dtype=tf.int32, name='initial_step'))
        update_step_fn = build_kalman_filter_step(self.get_transition_matrix_for_timestep, self.get_transition_noise_for_timestep, self.get_observation_matrix_for_timestep, self.get_observation_noise_for_timestep)
        filter_states = tf.scan(update_step_fn, elems=x if mask is None else (x, mask), initializer=initial_state)
        log_likelihoods = distribution_util.move_dimension(filter_states.log_marginal_likelihood, 0, -1)
        filtered_means = distribution_util.move_dimension(filter_states.filtered_mean[..., 0], 0, -2)
        filtered_covs = distribution_util.move_dimension(filter_states.filtered_cov, 0, -3)
        predicted_means = distribution_util.move_dimension(filter_states.predicted_mean[..., 0], 0, -2)
        predicted_covs = distribution_util.move_dimension(filter_states.predicted_cov, 0, -3)
        observation_means = distribution_util.move_dimension(filter_states.observation_mean[..., 0], 0, -2)
        observation_covs = distribution_util.move_dimension(filter_states.observation_cov, 0, -3)
        return (log_likelihoods, filtered_means, filtered_covs, predicted_means, predicted_covs, observation_means, observation_covs)