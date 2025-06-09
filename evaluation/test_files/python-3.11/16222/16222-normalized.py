def _download_http_url(link, session, temp_dir):
    """Download link url into temp_dir using provided session"""
    target_url = link.url.split('#', 1)[0]
    try:
        resp = session.get(target_url, headers={'Accept-Encoding': 'identity'}, stream=True)
        resp.raise_for_status()
    except requests.HTTPError as exc:
        logger.critical('HTTP error %s while getting %s', exc.response.status_code, link)
        raise
    content_type = resp.headers.get('content-type', '')
    filename = link.filename
    content_disposition = resp.headers.get('content-disposition')
    if content_disposition:
        type, params = cgi.parse_header(content_disposition)
        filename = params.get('filename') or filename
    ext = splitext(filename)[1]
    if not ext:
        ext = mimetypes.guess_extension(content_type)
        if ext:
            filename += ext
    if not ext and link.url != resp.url:
        ext = os.path.splitext(resp.url)[1]
        if ext:
            filename += ext
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, 'wb') as content_file:
        _download_url(resp, link, content_file)
    return (file_path, content_type)