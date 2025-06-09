def flatten(subject, test=None):
    """
	*Deprecated*: Use more_itertools.collapse instead.
	"""
    warnings.warn('Use more_itertools.collapse instead', DeprecationWarning, stacklevel=2)
    return list(more_itertools.collapse(subject, base_type=(bytes,)))