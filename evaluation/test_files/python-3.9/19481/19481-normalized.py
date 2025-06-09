def date(start, end):
    """Get a random date between two dates"""
    stime = date_to_timestamp(start)
    etime = date_to_timestamp(end)
    ptime = stime + random.random() * (etime - stime)
    return datetime.date.fromtimestamp(ptime)