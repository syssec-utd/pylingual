def send_email(to, subject, html_content, files=None, dryrun=False, cc=None, bcc=None, mime_subtype='mixed', mime_charset='utf-8', **kwargs):
    """
    Send email using backend specified in EMAIL_BACKEND.
    """
    path, attr = configuration.conf.get('email', 'EMAIL_BACKEND').rsplit('.', 1)
    module = importlib.import_module(path)
    backend = getattr(module, attr)
    to = get_email_address_list(to)
    to = ', '.join(to)
    return backend(to, subject, html_content, files=files, dryrun=dryrun, cc=cc, bcc=bcc, mime_subtype=mime_subtype, mime_charset=mime_charset, **kwargs)