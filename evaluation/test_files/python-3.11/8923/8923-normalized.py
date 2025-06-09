def runcode(obj, code_obj):
    """Execute a code object.

    When an exception occurs, self.showtraceback() is called to
    display a traceback.  All exceptions are caught except
    SystemExit, which is reraised.

    A note about KeyboardInterrupt: this exception may occur
    elsewhere in this code, and may not always be caught.  The
    caller should be prepared to deal with it.

    """
    try:
        exec(code_obj, obj.locals, obj.globals)
    except SystemExit:
        raise
    except:
        info = sys.exc_info()
        print('%s; %s' % (info[0], info[1]))
    else:
        pass
    return