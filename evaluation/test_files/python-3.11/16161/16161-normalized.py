def user_log_dir(appname):
    """
    Return full path to the user-specific log dir for this application.

        "appname" is the name of application.
            If None, just the system directory is returned.

    Typical user cache directories are:
        Mac OS X:   ~/Library/Logs/<AppName>
        Unix:       ~/.cache/<AppName>/log  # or under $XDG_CACHE_HOME if
                    defined
        Win XP:     C:\\Documents and Settings\\<username>\\Local Settings\\ ...
                    ...Application Data\\<AppName>\\Logs
        Vista:      C:\\Users\\<username>\\AppData\\Local\\<AppName>\\Logs

    On Windows the only suggestion in the MSDN docs is that local settings
    go in the `CSIDL_LOCAL_APPDATA` directory. (Note: I'm interested in
    examples of what some windows apps use for a logs dir.)

    OPINION: This function appends "Logs" to the `CSIDL_LOCAL_APPDATA`
    value for Windows and appends "log" to the user cache dir for Unix.
    """
    if WINDOWS:
        path = os.path.join(user_data_dir(appname), 'Logs')
    elif sys.platform == 'darwin':
        path = os.path.join(os.path.expanduser('~/Library/Logs'), appname)
    else:
        path = os.path.join(user_cache_dir(appname), 'log')
    return path