def cholesky_covariance(x, sample_axis=0, keepdims=False, name=None):
    """Cholesky factor of the covariance matrix of vector-variate random samples.

  This function can be use to fit a multivariate normal to data.

  ```python
  tf.enable_eager_execution()
  import tensorflow_probability as tfp
  tfd = tfp.distributions

  # Assume data.shape = (1000, 2).  1000 samples of a random variable in R^2.
  observed_data = read_data_samples(...)

  # The mean is easy
  mu = tf.reduce_mean(observed_data, axis=0)

  # Get the scale matrix
  L = tfp.stats.cholesky_covariance(observed_data)

  # Make the best fit multivariate normal (under maximum likelihood condition).
  mvn = tfd.MultivariateNormalTriL(loc=mu, scale_tril=L)

  # Plot contours of the pdf.
  xs, ys = tf.meshgrid(
      tf.linspace(-5., 5., 50), tf.linspace(-5., 5., 50), indexing='ij')
  xy = tf.stack((tf.reshape(xs, [-1]), tf.reshape(ys, [-1])), axis=-1)
  pdf = tf.reshape(mvn.prob(xy), (50, 50))
  CS = plt.contour(xs, ys, pdf, 10)
  plt.clabel(CS, inline=1, fontsize=10)
  ```

  Why does this work?
  Given vector-variate random variables `X = (X1, ..., Xd)`, one may obtain the
  sample covariance matrix in `R^{d x d}` (see `tfp.stats.covariance`).

  The [Cholesky factor](https://en.wikipedia.org/wiki/Cholesky_decomposition)
  of this matrix is analogous to standard deviation for scalar random variables:
  Suppose `X` has covariance matrix `C`, with Cholesky factorization `C = L L^T`
  Then multiplying a vector of iid random variables which have unit variance by
  `L` produces a vector with covariance `L L^T`, which is the same as `X`.

  ```python
  observed_data = read_data_samples(...)
  L = tfp.stats.cholesky_covariance(observed_data, sample_axis=0)

  # Make fake_data with the same covariance as observed_data.
  uncorrelated_normal = tf.random_normal(shape=(500, 10))
  fake_data = tf.linalg.matvec(L, uncorrelated_normal)
  ```

  Args:
    x:  Numeric `Tensor`.  The rightmost dimension of `x` indexes events. E.g.
      dimensions of a random vector.
    sample_axis: Scalar or vector `Tensor` designating axis holding samples.
      Default value: `0` (leftmost dimension). Cannot be the rightmost dimension
        (since this indexes events).
    keepdims:  Boolean.  Whether to keep the sample axis as singletons.
    name: Python `str` name prefixed to Ops created by this function.
          Default value: `None` (i.e., `'covariance'`).

  Returns:
    chol:  `Tensor` of same `dtype` as `x`.  The last two dimensions hold
      lower triangular matrices (the Cholesky factors).
  """
    with tf.compat.v1.name_scope(name, 'cholesky_covariance', values=[x, sample_axis]):
        sample_axis = tf.convert_to_tensor(value=sample_axis, dtype=tf.int32)
        cov = covariance(x, sample_axis=sample_axis, event_axis=-1, keepdims=keepdims)
        return tf.linalg.cholesky(cov)