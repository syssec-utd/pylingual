def log_errors(f, self, *args, **kwargs):
    """decorator to log unhandled exceptions raised in a method.
    
    For use wrapping on_recv callbacks, so that exceptions
    do not cause the stream to be closed.
    """
    try:
        return f(self, *args, **kwargs)
    except Exception:
        self.log.error('Uncaught exception in %r' % f, exc_info=True)