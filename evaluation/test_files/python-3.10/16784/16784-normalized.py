def mask(cls, dt, firstweekday=calendar.SATURDAY, **options):
    """
        Return a datetime with the same value as ``dt``, to a
        resolution of weeks.

        ``firstweekday`` determines when the week starts. It defaults
        to Saturday.
        """
    correction = (dt.weekday() - firstweekday) % cls.DAYS_IN_WEEK
    week = dt - timedelta(days=correction)
    return week.replace(hour=0, minute=0, second=0, microsecond=0)