def _inject_cookie_message(self, msg):
    """Inject the first message, which is the document cookie,
        for authentication."""
    if isinstance(msg, unicode):
        msg = msg.encode('utf8', 'replace')
    try:
        self.request._cookies = Cookie.SimpleCookie(msg)
    except:
        logging.warn("couldn't parse cookie string: %s", msg, exc_info=True)