def _any_match(matchers, record):
    """return the bool of whether `record` starts with
        any item in `matchers`"""

    def record_matches_key(key):
        return record == key or record.startswith(key + '.')
    return anyp(bool, map(record_matches_key, matchers))