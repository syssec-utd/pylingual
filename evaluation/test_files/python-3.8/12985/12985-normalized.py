def record_error(hostname, exc_info, preceding_stack=None, error_threshold=None, additional_info=None):
    """ Helper function to record errors to the flawless backend """
    stack = []
    (exc_type, exc_value, sys_traceback) = exc_info
    while sys_traceback is not None:
        stack.append(sys_traceback)
        sys_traceback = sys_traceback.tb_next
    stack_lines = []
    for row in preceding_stack or []:
        stack_lines.append(api_ttypes.StackLine(filename=os.path.abspath(row[0]), line_number=row[1], function_name=row[2], text=row[3]))
    for (index, tb) in enumerate(stack):
        filename = tb.tb_frame.f_code.co_filename
        func_name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        line = linecache.getline(filename, lineno, tb.tb_frame.f_globals)
        frame_locals = None
        if index >= len(stack) - NUM_FRAMES_TO_SAVE:
            frame_locals = dict(((k, _myrepr(k, v)) for (k, v) in list(tb.tb_frame.f_locals.items())[:MAX_LOCALS] if k != 'self'))
            if 'self' in tb.tb_frame.f_locals and hasattr(tb.tb_frame.f_locals['self'], '__dict__'):
                frame_locals.update(dict((('self.' + k, _myrepr(k, v)) for (k, v) in list(tb.tb_frame.f_locals['self'].__dict__.items())[:MAX_LOCALS] if k != 'self')))
        stack_lines.append(api_ttypes.StackLine(filename=os.path.abspath(filename), line_number=lineno, function_name=func_name, text=line, frame_locals=frame_locals))
    key = CachedErrorInfo.get_hash_key(stack_lines)
    info = ERROR_CACHE.get(key) or CachedErrorInfo()
    info.increment()
    ERROR_CACHE[key] = info
    if info.should_report():
        error_count = info.mark_reported()
        _send_request(api_ttypes.RecordErrorRequest(traceback=stack_lines, exception_message=repr(exc_value), exception_type=exc_type.__module__ + '.' + exc_type.__name__, hostname=hostname, error_threshold=error_threshold, additional_info=additional_info, error_count=error_count))