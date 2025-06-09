def repeated(extractor, times, *, ignore_whitespace=False):
    """Returns a partial of _get_repetition with bounds set to (times, times) that accepts only a text
  argument.
  """
    return partial(_get_repetition, extractor, bounds=(times, times), ignore_whitespace=ignore_whitespace)