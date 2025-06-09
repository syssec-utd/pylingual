def calc_expiry_time(minutes_valid):
    """Return specific time an auth_hash will expire."""
    return (timezone.now() + datetime.timedelta(minutes=minutes_valid + 1)).replace(second=0, microsecond=0)