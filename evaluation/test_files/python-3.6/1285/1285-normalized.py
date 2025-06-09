def _kl_laplace_laplace(a, b, name=None):
    """Calculate the batched KL divergence KL(a || b) with a and b Laplace.

  Args:
    a: instance of a Laplace distribution object.
    b: instance of a Laplace distribution object.
    name: (optional) Name to use for created operations.
      default is "kl_laplace_laplace".

  Returns:
    Batchwise KL(a || b)
  """
    with tf.name_scope(name or 'kl_laplace_laplace'):
        distance = tf.abs(a.loc - b.loc)
        ratio = a.scale / b.scale
        return -tf.math.log(ratio) - 1 + distance / b.scale + ratio * tf.exp(-distance / a.scale)