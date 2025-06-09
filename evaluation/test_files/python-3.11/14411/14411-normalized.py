def password_reset_email_handler(notification):
    """Password reset email handler."""
    base_subject = _('{domain} password reset').format(domain=notification.site.domain)
    subject = getattr(settings, 'DUM_PASSWORD_RESET_SUBJECT', base_subject)
    notification.email_subject = subject
    email_handler(notification, password_reset_email_context)