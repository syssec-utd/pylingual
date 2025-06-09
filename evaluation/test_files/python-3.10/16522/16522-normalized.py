def add_months(months, timestamp=datetime.datetime.utcnow()):
    """Add a number of months to a timestamp"""
    month = timestamp.month
    new_month = month + months
    years = 0
    while new_month < 1:
        new_month += 12
        years -= 1
    while new_month > 12:
        new_month -= 12
        years += 1
    year = timestamp.year + years
    try:
        return datetime.datetime(year, new_month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    except ValueError:
        if months > 0:
            new_month += 1
            if new_month > 12:
                new_month -= 12
                year += 1
            return datetime.datetime(year, new_month, 1, timestamp.hour, timestamp.minute, timestamp.second)
        else:
            new_day = calendar.monthrange(year, new_month)[1]
            return datetime.datetime(year, new_month, new_day, timestamp.hour, timestamp.minute, timestamp.second)