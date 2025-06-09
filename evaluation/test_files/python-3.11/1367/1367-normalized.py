def linear_gaussian_update(prior_mean, prior_cov, observation_matrix, observation_noise, x_observed):
    """Conjugate update for a linear Gaussian model.

  Given a normal prior on a latent variable `z`,
    `p(z) = N(prior_mean, prior_cov) = N(u, P)`,
  for which we observe a linear Gaussian transformation `x`,
    `p(x|z) = N(H * z + c, R)`,
  the posterior is also normal:
    `p(z|x) = N(u*, P*)`.

  We can write this update as
     x_expected = H * u + c # pushforward prior mean
     S = R + H * P * H'  # pushforward prior cov
     K = P * H' * S^{-1} # optimal Kalman gain
     u* = u + K * (x_observed - x_expected) # posterior mean
     P* = (I - K * H) * P (I - K * H)' + K * R * K' # posterior cov
  (see, e.g., https://en.wikipedia.org/wiki/Kalman_filter#Update)

  Args:
    prior_mean: `Tensor` with event shape `[latent_size, 1]` and
      potential batch shape `B = [b1, ..., b_n]`.
    prior_cov: `Tensor` with event shape `[latent_size, latent_size]`
      and batch shape `B` (matching `prior_mean`).
    observation_matrix: `LinearOperator` with shape
      `[observation_size, latent_size]` and batch shape broadcastable
      to `B`.
    observation_noise: potentially-batched
      `MultivariateNormalLinearOperator` instance with event shape
      `[observation_size]` and batch shape broadcastable to `B`.
    x_observed: potentially batched `Tensor` with event shape
      `[observation_size, 1]` and batch shape `B`.

  Returns:
    posterior_mean: `Tensor` with event shape `[latent_size, 1]` and
      batch shape `B`.
    posterior_cov: `Tensor` with event shape `[latent_size,
      latent_size]` and batch shape `B`.
    predictive_dist: the prior predictive distribution `p(x|z)`,
      as a `Distribution` instance with event
      shape `[observation_size]` and batch shape `B`. This will
      typically be `tfd.MultivariateNormalTriL`, but when
      `observation_size=1` we return a `tfd.Independent(tfd.Normal)`
      instance as an optimization.
  """
    observation_size_is_static_and_scalar = tf.compat.dimension_value(observation_matrix.shape[-2]) == 1
    x_expected = _propagate_mean(prior_mean, observation_matrix, observation_noise)
    tmp_obs_cov = observation_matrix.matmul(prior_cov)
    predicted_obs_cov = observation_matrix.matmul(tmp_obs_cov, adjoint_arg=True) + observation_noise.covariance()
    if observation_size_is_static_and_scalar:
        gain_transpose = tmp_obs_cov / predicted_obs_cov
    else:
        predicted_obs_cov_chol = tf.linalg.cholesky(predicted_obs_cov)
        gain_transpose = tf.linalg.cholesky_solve(predicted_obs_cov_chol, tmp_obs_cov)
    posterior_mean = prior_mean + tf.linalg.matmul(gain_transpose, x_observed - x_expected, adjoint_a=True)
    tmp_term = -observation_matrix.matmul(gain_transpose, adjoint=True)
    tmp_term = tf.linalg.set_diag(tmp_term, tf.linalg.diag_part(tmp_term) + 1)
    posterior_cov = tf.linalg.matmul(tmp_term, tf.linalg.matmul(prior_cov, tmp_term), adjoint_a=True) + tf.linalg.matmul(gain_transpose, tf.linalg.matmul(observation_noise.covariance(), gain_transpose), adjoint_a=True)
    if observation_size_is_static_and_scalar:
        predictive_dist = independent.Independent(normal.Normal(loc=x_expected[..., 0], scale=tf.sqrt(predicted_obs_cov[..., 0])), reinterpreted_batch_ndims=1)
        predictive_dist.covariance = lambda: predicted_obs_cov
    else:
        predictive_dist = mvn_tril.MultivariateNormalTriL(loc=x_expected[..., 0], scale_tril=predicted_obs_cov_chol)
    return (posterior_mean, posterior_cov, predictive_dist)