def _send_offer_assignment_notification_email(config, user_email, subject, email_body, site_code, task):
    """Handles sending offer assignment notification emails and retrying failed emails when appropriate."""
    try:
        sailthru_client = get_sailthru_client(site_code)
    except SailthruError:
        logger.exception('[Offer Assignment] A client error occurred while attempting to send a offer assignment notification. Message: {message}'.format(message=email_body))
        return None
    email_vars = {'subject': subject, 'email_body': email_body}
    try:
        response = sailthru_client.send(template=config['templates']['assignment_email'], email=user_email, _vars=email_vars)
    except SailthruClientError:
        logger.exception('[Offer Assignment] A client error occurred while attempting to send a offer assignment notification. Message: {message}'.format(message=email_body))
        return None
    if not response.is_ok():
        error = response.get_error()
        logger.error('[Offer Assignment] A {token_error_code} - {token_error_message} error occurred while attempting to send a offer assignment notification. Message: {message}'.format(message=email_body, token_error_code=error.get_error_code(), token_error_message=error.get_message()))
        if can_retry_sailthru_request(error):
            logger.info('[Offer Assignment] An attempt will be made to resend the offer assignment notification. Message: {message}'.format(message=email_body))
            schedule_retry(task, config)
        else:
            logger.warning('[Offer Assignment] No further attempts will be made to send the offer assignment notification. Failed Message: {message}'.format(message=email_body))
    return response