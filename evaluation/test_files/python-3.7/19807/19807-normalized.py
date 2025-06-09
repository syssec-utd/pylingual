def setup_logging(log_filename=None, log_level='DEBUG', str_format=None, date_format=None, log_file_level='DEBUG', log_stdout_level=None, log_restart=False, log_history=False, formatter=None, silence_modules=None, log_filter=None):
    """
    This will setup logging for a single file but can be called more than once
    LOG LEVELS are "CRITICAL", "ERROR", "INFO", "DEBUG"
    :param log_filename:    str of the file location
    :param log_level:       str of the overall logging level for setLevel
    :param str_format:      str of the logging format
    :param date_format:     str of the date format
    :param log_file_level   str of the log level to use on this file
    :param log_stdout_level str of the log level to use on this file
                            (None means no stdout logging)
    :param log_restart:     bool if True the log file will be deleted first
    :param log_history:     bool if True will save another log file in a
                            folder called history with the datetime
    :param formatter:       logging.Format instance to use
    :param silence_modules  list of str of modules to silence
    :param log_filter:      logging.filter instance to add to handler
    :return:                None
    """
    setup_log_level(log_level)
    if log_filename:
        setup_file_logging(log_filename=log_filename, str_format=str_format, log_history=log_history, formatter=formatter, log_file_level=log_file_level, log_restart=log_restart, date_format=date_format, log_filter=log_filter)
    if log_stdout_level is not None:
        setup_stdout_logging(log_level=log_level, log_stdout_level=log_stdout_level, str_format=str_format, date_format=date_format, formatter=formatter, log_filter=log_filter)
    silence_module_logging(silence_modules)