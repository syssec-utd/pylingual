def _moment(self, n):
    """Compute the n'th (uncentered) moment."""
    total_concentration = self.concentration1 + self.concentration0
    expanded_concentration1 = tf.ones_like(total_concentration, dtype=self.dtype) * self.concentration1
    expanded_concentration0 = tf.ones_like(total_concentration, dtype=self.dtype) * self.concentration0
    beta_arg0 = 1 + n / expanded_concentration1
    beta_arg = tf.stack([beta_arg0, expanded_concentration0], -1)
    log_moment = tf.math.log(expanded_concentration0) + tf.math.lbeta(beta_arg)
    return tf.exp(log_moment)