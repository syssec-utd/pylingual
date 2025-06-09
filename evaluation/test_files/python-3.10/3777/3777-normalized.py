def shift(schedule: ScheduleComponent, time: int, name: str=None) -> Schedule:
    """Return schedule shifted by `time`.

    Args:
        schedule: The schedule to shift
        time: The time to shift by
        name: Name of shifted schedule. Defaults to name of `schedule`
    """
    if name is None:
        name = schedule.name
    return union((time, schedule), name=name)