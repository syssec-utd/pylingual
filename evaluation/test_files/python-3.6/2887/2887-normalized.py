def format_time(elapsed):
    """Formats elapsed seconds into a human readable format."""
    hours = int(elapsed / (60 * 60))
    minutes = int(elapsed % (60 * 60) / 60)
    seconds = int(elapsed % 60)
    rval = ''
    if hours:
        rval += '{0}h'.format(hours)
    if elapsed > 60:
        rval += '{0}m'.format(minutes)
    rval += '{0}s'.format(seconds)
    return rval