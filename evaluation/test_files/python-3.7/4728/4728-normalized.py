def _parse_retry_after(self, response):
    """Parse Retry-After header from response if it is set."""
    value = response.headers.get('Retry-After')
    if not value:
        seconds = 0
    elif re.match('^\\s*[0-9]+\\s*$', value):
        seconds = int(value)
    else:
        date_tuple = email.utils.parsedate(value)
        if date_tuple is None:
            seconds = 0
        else:
            seconds = time.mktime(date_tuple) - time.time()
    return max(0, seconds)