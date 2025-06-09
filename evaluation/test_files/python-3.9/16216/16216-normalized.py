def debug_application(self, environ, start_response):
    """Run the application and conserve the traceback frames."""
    app_iter = None
    try:
        app_iter = self.app(environ, start_response)
        for item in app_iter:
            yield item
        if hasattr(app_iter, 'close'):
            app_iter.close()
    except Exception:
        if hasattr(app_iter, 'close'):
            app_iter.close()
        traceback = get_current_traceback(skip=1, show_hidden_frames=self.show_hidden_frames, ignore_system_exceptions=True)
        for frame in traceback.frames:
            self.frames[frame.id] = frame
        self.tracebacks[traceback.id] = traceback
        try:
            start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/html; charset=utf-8'), ('X-XSS-Protection', '0')])
        except Exception:
            environ['wsgi.errors'].write('Debugging middleware caught exception in streamed response at a point where response headers were already sent.\n')
        else:
            yield traceback.render_full(evalex=self.evalex, secret=self.secret).encode('utf-8', 'replace')
        traceback.log(environ['wsgi.errors'])