def top(self):
    """
        Property.
        """
    with warnings.catch_warnings():
        warnings.simplefilter('always')
        w = 'Striplog.top is deprecated; please use Striplog.unique'
        warnings.warn(w, DeprecationWarning, stacklevel=2)
    return self.unique