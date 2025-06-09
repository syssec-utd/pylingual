def position_from_bundle(self, bundle):
    """[DEPRECATED] Return position, given the `coefficient_bundle()` return value."""
    (coefficients, days_per_set, T, twot1) = bundle
    return (T.T * coefficients).sum(axis=2)