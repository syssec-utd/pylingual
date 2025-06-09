def handle_exception(self, exc_info=None, state=None, tags=None, return_feedback_urls=False, dry_run=False):
    """
        Call this method from within a try/except clause to generate a call to Stack Sentinel.

        :param exc_info: Return value of sys.exc_info(). If you pass None, handle_exception will call sys.exc_info() itself
        :param state: Dictionary of state information associated with the error. This could be form data, cookie data, whatnot. NOTE: sys and machine are added to this dictionary if they are not already included.
        :param tags: Any string tags you want associated with the exception report.
        :param return_feedback_urls: If True, Stack Sentinel will return feedback URLs you can present to the user for extra debugging information.
        :param dry_run: If True, method will not actively send in error information to API. Instead, it will return a request object and payload. Used in unittests.

        """
    if not exc_info:
        exc_info = sys.exc_info()
    if exc_info is None:
        raise StackSentinelError('handle_exception called outside of exception handler')
    (etype, value, tb) = exc_info
    try:
        msg = value.args[0]
    except:
        msg = repr(value)
    if not isinstance(tags, list):
        tags = [tags]
    limit = None
    new_tb = []
    n = 0
    while tb is not None and (limit is None or n < limit):
        f = tb.tb_frame
        lineno = tb.tb_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        tb = tb.tb_next
        n = n + 1
        new_tb.append({'line': lineno, 'module': filename, 'method': name})
    if state is None:
        state = {}
    if 'sys' not in state:
        try:
            state['sys'] = self._get_sys_info()
        except Exception as e:
            state['sys'] = '<Unable to get sys: %r>' % e
    if 'machine' not in state:
        try:
            state['machine'] = self._get_machine_info()
        except Exception as e:
            state['machine'] = '<Unable to get machine: %e>' % e
    if tags is None:
        tags = []
    if sys.version_info.major > 2:
        error_type = str(etype.__name__)
        error_message = str(value)
    else:
        error_type = unicode(etype.__name__)
        error_message = unicode(value)
    send_error_args = dict(error_type=error_type, error_message=error_message, traceback=new_tb, environment=self.environment, state=state, tags=self.tags + tags, return_feedback_urls=return_feedback_urls)
    if dry_run:
        return send_error_args
    else:
        return self.send_error(**send_error_args)