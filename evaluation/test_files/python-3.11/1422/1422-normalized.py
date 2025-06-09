def _maybe_validate_target_accept_prob(target_accept_prob, validate_args):
    """Validates that target_accept_prob is in (0, 1)."""
    if not validate_args:
        return target_accept_prob
    with tf.control_dependencies([tf.compat.v1.assert_positive(target_accept_prob, message='`target_accept_prob` must be > 0.'), tf.compat.v1.assert_less(target_accept_prob, tf.ones_like(target_accept_prob), message='`target_accept_prob` must be < 1.')]):
        return tf.identity(target_accept_prob)