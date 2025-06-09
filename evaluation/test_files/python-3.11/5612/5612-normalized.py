def format_section(stream, section, options, doc=None):
    """format an options section using the INI format"""
    if doc:
        print(_comment(doc), file=stream)
    print('[%s]' % section, file=stream)
    _ini_format(stream, options)