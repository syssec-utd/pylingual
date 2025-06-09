def _clean_longitudinal_data(cls, data, null=None):
    """
        Private function. Make sure we have what we need to make a striplog.
        """
    if 'top' not in data.keys():
        data['top'] = data.pop('depth', data.pop('MD', None))
    idx = list(data.keys()).index('top')
    values = sorted(zip(*data.values()), key=lambda x: x[idx])
    data = {k: list(v) for k, v in zip(data.keys(), zip(*values))}
    if data['top'] is None:
        raise StriplogError('Could not get tops.')
    if null is not None:
        for k, v in data.items():
            data[k] = [i if i != null else None for i in v]
    return data