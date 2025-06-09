def url_(client_id: str, redirect_uri: str, *, scope: str=None, state: str=None, secure: bool=True) -> str:
    """Construct a OAuth2 URL instead of an OAuth2 object."""
    attrs = {'client_id': client_id, 'redirect_uri': quote(redirect_uri)}
    if scope is not None:
        attrs['scope'] = quote(scope)
    if state is not None:
        attrs['state'] = state
    parameters = '&'.join(('{0}={1}'.format(*item) for item in attrs.items()))
    return OAuth2._BASE.format(parameters=parameters)