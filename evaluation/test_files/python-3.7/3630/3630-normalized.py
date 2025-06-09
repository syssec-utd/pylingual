async def async_send(self, request, headers=None, content=None, **config):
    """Prepare and send request object according to configuration.
        :param ClientRequest request: The request object to be sent.
        :param dict headers: Any headers to add to the request.
        :param content: Any body data to add to the request.
        :param config: Any specific config overrides
        """
    loop = asyncio.get_event_loop()
    if self.config.keep_alive and self._session is None:
        self._session = requests.Session()
    try:
        session = self.creds.signed_session(self._session)
    except TypeError:
        session = self.creds.signed_session()
        if self._session is not None:
            _LOGGER.warning('Your credentials class does not support session injection. Performance will not be at the maximum.')
    kwargs = self._configure_session(session, **config)
    if headers:
        request.headers.update(headers)
    if not kwargs.get('files'):
        request.add_content(content)
    if request.data:
        kwargs['data'] = request.data
    kwargs['headers'].update(request.headers)
    response = None
    try:
        try:
            future = loop.run_in_executor(None, functools.partial(session.request, request.method, request.url, **kwargs))
            return await future
        except (oauth2.rfc6749.errors.InvalidGrantError, oauth2.rfc6749.errors.TokenExpiredError) as err:
            error = 'Token expired or is invalid. Attempting to refresh.'
            _LOGGER.warning(error)
        try:
            session = self.creds.refresh_session()
            kwargs = self._configure_session(session)
            if request.data:
                kwargs['data'] = request.data
            kwargs['headers'].update(request.headers)
            future = loop.run_in_executor(None, functools.partial(session.request, request.method, request.url, **kwargs))
            return await future
        except (oauth2.rfc6749.errors.InvalidGrantError, oauth2.rfc6749.errors.TokenExpiredError) as err:
            msg = 'Token expired or is invalid.'
            raise_with_traceback(TokenExpiredError, msg, err)
    except (requests.RequestException, oauth2.rfc6749.errors.OAuth2Error) as err:
        msg = 'Error occurred in request.'
        raise_with_traceback(ClientRequestError, msg, err)
    finally:
        self._close_local_session_if_necessary(response, session, kwargs['stream'])