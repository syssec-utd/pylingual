def _kl_von_mises_von_mises(d1, d2, name=None):
    """Batchwise KL divergence KL(d1 || d2) with d1 and d2 von Mises.

  Args:
    d1: instance of a von Mises distribution object.
    d2: instance of a a von Mises distribution object.
    name: (optional) Name to use for created operations.
      default is "kl_von_mises_von_mises".

  Returns:
    Batchwise KL(d1 || d2)
  """
    with tf.name_scope(name or 'kl_von_mises_von_mises'):
        i0e_concentration1 = tf.math.bessel_i0e(d1.concentration)
        i1e_concentration1 = tf.math.bessel_i1e(d1.concentration)
        i0e_concentration2 = tf.math.bessel_i0e(d2.concentration)
        return d2.concentration - d1.concentration + tf.math.log(i0e_concentration2 / i0e_concentration1) + (d1.concentration - d2.concentration * tf.cos(d1.loc - d2.loc)) * (i1e_concentration1 / i0e_concentration1)