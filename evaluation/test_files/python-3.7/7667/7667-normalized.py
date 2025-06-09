def summary(self, fmt=None, initial=True, default=''):
    """
        Given a format string, return a summary description of a component.

        Args:
            component (dict): A component dictionary.
            fmt (str): Describes the format with a string. If no format is
                given, you will just get a list of attributes. If you give the
                empty string (''), you'll get `default` back. By default this
                gives you the empty string, effectively suppressing the
                summary.
            initial (bool): Whether to capitialize the first letter. Default is
                True.
            default (str): What to give if there's no component defined.

        Returns:
            str: A summary string.

        Example:

            r = Component({'colour': 'Red',
                           'grainsize': 'VF-F',
                           'lithology': 'Sandstone'})

            r.summary()  -->  'Red, vf-f, sandstone'
        """
    if default and (not self.__dict__):
        return default
    if fmt == '':
        return default
    keys = [k for (k, v) in self.__dict__.items() if v is not '']
    f = fmt or '{' + '}, {'.join(keys) + '}'
    try:
        summary = CustomFormatter().format(f, **self.__dict__)
    except KeyError as e:
        raise ComponentError('Error building summary, ' + str(e))
    if summary and initial and (not fmt):
        summary = summary[0].upper() + summary[1:]
    return summary