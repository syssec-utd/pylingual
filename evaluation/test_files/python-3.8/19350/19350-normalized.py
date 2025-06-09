def setup(level='debug', output=None):
    """ Hivy formated logger """
    output = output or settings.LOG['file']
    level = level.upper()
    handlers = [logbook.NullHandler()]
    if output == 'stdout':
        handlers.append(logbook.StreamHandler(sys.stdout, format_string=settings.LOG['format'], level=level))
    else:
        handlers.append(logbook.FileHandler(output, format_string=settings.LOG['format'], level=level))
    sentry_dns = settings.LOG['sentry_dns']
    if sentry_dns:
        handlers.append(SentryHandler(sentry_dns, level='ERROR'))
    return logbook.NestedSetup(handlers)