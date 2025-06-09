from datetime import time, datetime, timedelta
from neo4j.packstream import Structure
from neo4j.time import Duration, Date, Time, DateTime

def get_date_unix_epoch():
    return Date(1970, 1, 1)

def get_date_unix_epoch_ordinal():
    return get_date_unix_epoch().to_ordinal()

def get_datetime_unix_epoch_utc():
    from pytz import utc
    return DateTime(1970, 1, 1, 0, 0, 0, utc)

def hydrate_date(days):
    """ Hydrator for `Date` values.

    :param days:
    :return: Date
    """
    return Date.from_ordinal(get_date_unix_epoch_ordinal() + days)

def dehydrate_date(value):
    """ Dehydrator for `date` values.

    :param value:
    :type value: Date
    :return:
    """
    return Structure(b'D', value.toordinal() - get_date_unix_epoch().toordinal())

def hydrate_time(nanoseconds, tz=None):
    """ Hydrator for `Time` and `LocalTime` values.

    :param nanoseconds:
    :param tz:
    :return: Time
    """
    from pytz import FixedOffset
    (seconds, nanoseconds) = map(int, divmod(nanoseconds, 1000000000))
    (minutes, seconds) = map(int, divmod(seconds, 60))
    (hours, minutes) = map(int, divmod(minutes, 60))
    t = Time(hours, minutes, seconds, nanoseconds)
    if tz is None:
        return t
    (tz_offset_minutes, tz_offset_seconds) = divmod(tz, 60)
    zone = FixedOffset(tz_offset_minutes)
    return zone.localize(t)

def dehydrate_time(value):
    """ Dehydrator for `time` values.

    :param value:
    :type value: Time
    :return:
    """
    if isinstance(value, Time):
        nanoseconds = value.ticks_ns
    elif isinstance(value, time):
        nanoseconds = 3600000000000 * value.hour + 60000000000 * value.minute + 1000000000 * value.second + 1000 * value.microsecond
    else:
        raise TypeError('Value must be a neo4j.time.Time or a datetime.time')
    if value.tzinfo:
        return Structure(b'T', nanoseconds, int(value.tzinfo.utcoffset(value).total_seconds()))
    else:
        return Structure(b't', nanoseconds)

def hydrate_datetime(seconds, nanoseconds, tz=None):
    """ Hydrator for `DateTime` and `LocalDateTime` values.

    :param seconds:
    :param nanoseconds:
    :param tz:
    :return: datetime
    """
    from pytz import FixedOffset, timezone
    (minutes, seconds) = map(int, divmod(seconds, 60))
    (hours, minutes) = map(int, divmod(minutes, 60))
    (days, hours) = map(int, divmod(hours, 24))
    t = DateTime.combine(Date.from_ordinal(get_date_unix_epoch_ordinal() + days), Time(hours, minutes, seconds, nanoseconds))
    if tz is None:
        return t
    if isinstance(tz, int):
        (tz_offset_minutes, tz_offset_seconds) = divmod(tz, 60)
        zone = FixedOffset(tz_offset_minutes)
    else:
        zone = timezone(tz)
    return zone.localize(t)

def hydrate_datetime_v2(seconds, nanoseconds, tz=None):
    """ Hydrator for `DateTime` and `LocalDateTime` values.

    :param seconds:
    :param nanoseconds:
    :param tz:
    :return: datetime
    """
    import pytz
    (minutes, seconds) = map(int, divmod(seconds, 60))
    (hours, minutes) = map(int, divmod(minutes, 60))
    (days, hours) = map(int, divmod(hours, 24))
    t = DateTime.combine(Date.from_ordinal(get_date_unix_epoch_ordinal() + days), Time(hours, minutes, seconds, nanoseconds))
    if tz is None:
        return t
    if isinstance(tz, int):
        (tz_offset_minutes, tz_offset_seconds) = divmod(tz, 60)
        zone = pytz.FixedOffset(tz_offset_minutes)
    else:
        zone = pytz.timezone(tz)
    t = t.replace(tzinfo=pytz.UTC)
    return t.as_timezone(zone)

def dehydrate_datetime(value):
    """ Dehydrator for `datetime` values.

    :param value:
    :type value: datetime
    :return:
    """

    def seconds_and_nanoseconds(dt):
        if isinstance(dt, datetime):
            dt = DateTime.from_native(dt)
        zone_epoch = DateTime(1970, 1, 1, tzinfo=dt.tzinfo)
        dt_clock_time = dt.to_clock_time()
        zone_epoch_clock_time = zone_epoch.to_clock_time()
        t = dt_clock_time - zone_epoch_clock_time
        return (t.seconds, t.nanoseconds)
    tz = value.tzinfo
    if tz is None:
        from pytz import utc
        value = utc.localize(value)
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        return Structure(b'd', seconds, nanoseconds)
    elif hasattr(tz, 'zone') and tz.zone and isinstance(tz.zone, str):
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        return Structure(b'f', seconds, nanoseconds, tz.zone)
    elif hasattr(tz, 'key') and tz.key and isinstance(tz.key, str):
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        return Structure(b'f', seconds, nanoseconds, tz.key)
    else:
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        offset = tz.utcoffset(value)
        if offset.microseconds:
            raise ValueError('Bolt protocol does not support sub-second UTC offsets.')
        offset_seconds = offset.days * 86400 + offset.seconds
        return Structure(b'F', seconds, nanoseconds, offset_seconds)

def dehydrate_datetime_v2(value):
    """ Dehydrator for `datetime` values.

    :param value:
    :type value: datetime
    :return:
    """
    import pytz

    def seconds_and_nanoseconds(dt):
        if isinstance(dt, datetime):
            dt = DateTime.from_native(dt)
        dt = dt.astimezone(pytz.UTC)
        utc_epoch = DateTime(1970, 1, 1, tzinfo=pytz.UTC)
        dt_clock_time = dt.to_clock_time()
        utc_epoch_clock_time = utc_epoch.to_clock_time()
        t = dt_clock_time - utc_epoch_clock_time
        return (t.seconds, t.nanoseconds)
    tz = value.tzinfo
    if tz is None:
        value = pytz.UTC.localize(value)
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        return Structure(b'd', seconds, nanoseconds)
    elif hasattr(tz, 'zone') and tz.zone and isinstance(tz.zone, str):
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        return Structure(b'i', seconds, nanoseconds, tz.zone)
    elif hasattr(tz, 'key') and tz.key and isinstance(tz.key, str):
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        return Structure(b'i', seconds, nanoseconds, tz.key)
    else:
        (seconds, nanoseconds) = seconds_and_nanoseconds(value)
        offset = tz.utcoffset(value)
        if offset.microseconds:
            raise ValueError('Bolt protocol does not support sub-second UTC offsets.')
        offset_seconds = offset.days * 86400 + offset.seconds
        return Structure(b'I', seconds, nanoseconds, offset_seconds)

def hydrate_duration(months, days, seconds, nanoseconds):
    """ Hydrator for `Duration` values.

    :param months:
    :param days:
    :param seconds:
    :param nanoseconds:
    :return: `duration` namedtuple
    """
    return Duration(months=months, days=days, seconds=seconds, nanoseconds=nanoseconds)

def dehydrate_duration(value):
    """ Dehydrator for `duration` values.

    :param value:
    :type value: Duration
    :return:
    """
    return Structure(b'E', value.months, value.days, value.seconds, value.nanoseconds)

def dehydrate_timedelta(value):
    """ Dehydrator for `timedelta` values.

    :param value:
    :type value: timedelta
    :return:
    """
    months = 0
    days = value.days
    seconds = value.seconds
    nanoseconds = 1000 * value.microseconds
    return Structure(b'E', months, days, seconds, nanoseconds)