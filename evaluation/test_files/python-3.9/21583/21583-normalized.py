def inputhook_glut():
    """Run the pyglet event loop by processing pending events only.

    This keeps processing pending events until stdin is ready.  After
    processing all pending events, a call to time.sleep is inserted.  This is
    needed, otherwise, CPU usage is at 100%.  This sleep time should be tuned
    though for best performance.
    """
    signal.signal(signal.SIGINT, glut_int_handler)
    try:
        t = clock()
        if glut.glutGetWindow() == 0:
            glut.glutSetWindow(1)
            glutMainLoopEvent()
            return 0
        while not stdin_ready():
            glutMainLoopEvent()
            used_time = clock() - t
            if used_time > 5 * 60.0:
                time.sleep(5.0)
            elif used_time > 10.0:
                time.sleep(1.0)
            elif used_time > 0.1:
                time.sleep(0.05)
            else:
                time.sleep(0.001)
    except KeyboardInterrupt:
        pass
    return 0