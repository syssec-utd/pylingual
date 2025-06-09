def get_end_of_day(timestamp):
    """
    Given a date or a datetime, return a datetime at 23:59:59 on that day
    """
    return datetime.datetime(timestamp.year, timestamp.month, timestamp.day, 23, 59, 59)