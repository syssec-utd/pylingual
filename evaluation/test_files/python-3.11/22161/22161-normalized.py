def start_event_loop_qt4(app=None):
    """Start the qt4 event loop in a consistent manner."""
    if app is None:
        app = get_app_qt4([''])
    if not is_event_loop_running_qt4(app):
        app._in_event_loop = True
        app.exec_()
        app._in_event_loop = False
    else:
        app._in_event_loop = True