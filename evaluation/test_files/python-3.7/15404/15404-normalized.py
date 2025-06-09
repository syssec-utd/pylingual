def send_confirmed_notifications(request):
    """Receiver for request-confirmed signal to send email notification."""
    (pid, record) = get_record(request.recid)
    if record is None:
        current_app.logger.error('Cannot retrieve record %s. Emails not sent' % request.recid)
        return
    title = _('Access request: %(record)s', record=record['title'])
    _send_notification(request.receiver.email, title, 'zenodo_accessrequests/emails/new_request.tpl', request=request, record=record, pid=pid)
    _send_notification(request.sender_email, title, 'zenodo_accessrequests/emails/confirmation.tpl', request=request, record=record, pid=pid)