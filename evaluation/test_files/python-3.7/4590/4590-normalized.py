def user_code_error_boundary(error_cls, msg, **kwargs):
    """
    Wraps the execution of user-space code in an error boundary. This places a uniform
    policy around an user code invoked by the framework. This ensures that all user
    errors are wrapped in the DagsterUserCodeExecutionError, and that the original stack
    trace of the user error is preserved, so that it can be reported without confusing
    framework code in the stack trace, if a tool author wishes to do so. This has
    been especially help in a notebooking context.
    """
    check.str_param(msg, 'msg')
    check.subclass_param(error_cls, 'error_cls', DagsterUserCodeExecutionError)
    try:
        yield
    except Exception as e:
        if isinstance(e, DagsterError):
            raise e
        else:
            raise_from(error_cls(msg, user_exception=e, original_exc_info=sys.exc_info(), **kwargs), e)