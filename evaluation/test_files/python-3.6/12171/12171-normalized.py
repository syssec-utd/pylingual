def recording_state(recording_id, status):
    """Send the state of the current recording to the Matterhorn core.

    :param recording_id: ID of the current recording
    :param status: Status of the recording
    """
    if config()['agent']['backup_mode']:
        return
    params = [('state', status)]
    url = config()['service-capture.admin'][0]
    url += '/recordings/%s' % recording_id
    try:
        result = http_request(url, params)
        logger.info(result)
    except pycurl.error as e:
        logger.warning('Could not set recording state to %s: %s' % (status, e))