def _record_purchase(sailthru_client, email, item, purchase_incomplete, message_id, options):
    """Record a purchase in Sailthru

    Arguments:
        sailthru_client (object): SailthruClient
        email (str): user's email address
        item (dict): Sailthru required information about the course
        purchase_incomplete (boolean): True if adding item to shopping cart
        message_id (str): Cookie used to identify marketing campaign
        options (dict): Sailthru purchase API options (e.g. template name)

    Returns:
        False if retryable error, else True
    """
    try:
        sailthru_response = sailthru_client.purchase(email, [item], incomplete=purchase_incomplete, message_id=message_id, options=options)
        if not sailthru_response.is_ok():
            error = sailthru_response.get_error()
            logger.error('Error attempting to record purchase in Sailthru: %s', error.get_message())
            return not can_retry_sailthru_request(error)
    except SailthruClientError as exc:
        logger.exception('Exception attempting to record purchase for %s in Sailthru - %s', email, text_type(exc))
        return False
    return True