def log(logger=None, start_message='Starting...', end_message='Done...'):
    """
    Basic log decorator
    Can be used as :
    - @log (with default logger)
    - @log(mylogger)
    - @log(start_message='Hello !", logger=mylogger, end_message='Bye !')
    """

    def actual_log(f, real_logger=logger):
        logger = real_logger or _logger

        @wraps(f)
        def timed(*args, **kwargs):
            logger.info(f'{f.__name__} - {start_message}')
            start = time.time()
            res = f(*args, **kwargs)
            end = time.time()
            logger.info(f'{f.__name__} - {end_message} (took {end - start:.2f}s)')
            return res
        return timed
    if callable(logger):
        return actual_log(logger, real_logger=None)
    return actual_log