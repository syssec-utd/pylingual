def _get_index_points(self, index_points=None):
    """Return `index_points` if not None, else `self._index_points`.

    Args:
      index_points: if given, this is what is returned; else,
      `self._index_points`

    Returns:
      index_points: the given arg, if not None, else the class member
      `self._index_points`.

    Rases:
      ValueError: if `index_points` and `self._index_points` are both `None`.
    """
    if self._index_points is None and index_points is None:
        raise ValueError("This GaussianProcess instance was not instantiated with a value for index_points. One must therefore be provided when calling sample, log_prob, and other such methods. In particular, one can't compute KL divergences to/from an instance of `GaussianProccess` with unspecified `index_points` directly. Instead, use the `get_marginal_distribution` function, which takes `index_points` as an argument and returns a `Normal` or `MultivariateNormalLinearOperator` instance, whose KL can be computed.")
    return index_points if index_points is not None else self._index_points