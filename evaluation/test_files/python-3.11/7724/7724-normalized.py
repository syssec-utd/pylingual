def convert_field(self, value, conversion):
    """
        Define some extra field conversion functions.
        """
    try:
        s = super(CustomFormatter, self)
        return s.convert_field(value, conversion)
    except ValueError:
        funcs = {'s': str, 'r': repr, 'a': ascii, 'u': str.upper, 'l': str.lower, 'c': str.capitalize, 't': str.title, 'm': np.mean, 'µ': np.mean, 'v': np.var, 'd': np.std, '+': np.sum, '∑': np.sum, 'x': np.product}
        return funcs.get(conversion)(value)