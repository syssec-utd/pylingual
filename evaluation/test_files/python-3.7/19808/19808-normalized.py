def setup_stdout_logging(log_level='DEBUG', log_stdout_level='DEBUG', str_format=None, date_format=None, formatter=None, silence_modules=None, log_filter=None):
    """
    This will setup logging for stdout and stderr
    :param formatter:
    :param log_level:        str of the overall logging level for setLevel
    :param log_stdout_level: str of the logging level of stdout
    :param str_format:       str of the logging format
    :param date_format:      str of the date format
    :param silence_modules:  list of str of modules to exclude from logging
    :param log_filter:       logging.filter instance to add to handler
    :return:                 None
    """
    setup_log_level(log_level)
    formatter = formatter or SeabornFormatter(str_format, date_format)
    if log_stdout_level != 'ERROR':
        stdout_handler = logging.StreamHandler(sys.__stdout__)
        add_handler(log_stdout_level, stdout_handler, formatter, NoErrorFilter())
    stderr_handler = logging.StreamHandler(sys.__stderr__)
    add_handler('ERROR', stderr_handler, formatter, log_filter)
    silence_module_logging(silence_modules)