def map(self, mapper, nan_mapping=None, null_mapping=None):
    """Map values of an expression or in memory column accoring to an input
        dictionary or a custom callable function.

        Example:

        >>> import vaex
        >>> df = vaex.from_arrays(color=['red', 'red', 'blue', 'red', 'green'])
        >>> mapper = {'red': 1, 'blue': 2, 'green': 3}
        >>> df['color_mapped'] = df.color.map(mapper)
        >>> df
        #  color      color_mapped
        0  red                   1
        1  red                   1
        2  blue                  2
        3  red                   1
        4  green                 3
        >>> import numpy as np
        >>> df = vaex.from_arrays(type=[0, 1, 2, 2, 2, np.nan])
        >>> df['role'] = df['type'].map({0: 'admin', 1: 'maintainer', 2: 'user', np.nan: 'unknown'})
        >>> df
        #    type  role
        0       0  admin
        1       1  maintainer
        2       2  user
        3       2  user
        4       2  user
        5     nan  unknown        

        :param mapper: dict like object used to map the values from keys to values
        :param nan_mapping: value to be used when a nan is present (and not in the mapper)
        :param null_mapping: value to use used when there is a missing value
        :return: A vaex expression
        :rtype: vaex.expression.Expression
        """
    assert isinstance(mapper, collectionsAbc.Mapping), 'mapper should be a dict like object'
    df = self.ds
    mapper_keys = np.array(list(mapper.keys()))
    key_set = df._set(self.expression)
    found_keys = key_set.keys()
    mapper_has_nan = any([key != key for key in mapper_keys])
    if not set(mapper_keys).issuperset(found_keys):
        missing = set(found_keys).difference(mapper_keys)
        missing0 = list(missing)[0]
        if missing0 == missing0:
            raise ValueError('Missing values in mapper: %s' % missing)
    choices = [mapper[key] for key in found_keys]
    if key_set.has_nan:
        if mapper_has_nan:
            choices = [mapper[np.nan]] + choices
        else:
            choices = [nan_mapping] + choices
    if key_set.has_null:
        choices = [null_mapping] + choices
    choices = np.array(choices)
    key_set_name = df.add_variable('map_key_set', key_set, unique=True)
    choices_name = df.add_variable('map_choices', choices, unique=True)
    expr = '_choose(_ordinal_values({}, {}), {})'.format(self, key_set_name, choices_name)
    return Expression(df, expr)