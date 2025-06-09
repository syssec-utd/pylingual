def _find_playlist_info(response):
    """
    Finds playlist info (type, id) in HTTP response.

    :param response: Response object.
    :returns: Dictionary with type and id.
    """
    values = {}
    matches = _playlist_info_re.search(response.text)
    if matches:
        values['type'] = matches.group(1)
        values['id'] = matches.group(2)
    return values