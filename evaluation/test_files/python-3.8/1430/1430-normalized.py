def _maybe_assert_valid_sample(self, counts):
    """Check counts for proper shape, values, then return tensor version."""
    if not self.validate_args:
        return counts
    counts = distribution_util.embed_check_nonnegative_integer_form(counts)
    return distribution_util.with_dependencies([assert_util.assert_equal(self.total_count, tf.reduce_sum(input_tensor=counts, axis=-1), message='counts last-dimension must sum to `self.total_count`')], counts)