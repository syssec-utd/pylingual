def _get_tls(self):
    """Get an SMTP session with TLS."""
    session = smtplib.SMTP(self.server, self.port)
    session.ehlo()
    session.starttls(context=ssl.create_default_context())
    session.ehlo()
    return session