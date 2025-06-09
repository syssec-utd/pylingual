def _variance_scale_term(self):
    """Helper to `_covariance` and `_variance` which computes a shared scale."""
    c0 = self.total_concentration[..., tf.newaxis]
    return tf.sqrt((1.0 + c0 / self.total_count[..., tf.newaxis]) / (1.0 + c0))