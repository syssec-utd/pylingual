def insert(self, start_time: int, schedule: ScheduleComponent) -> 'ScheduleComponent':
    """Return a new schedule with `schedule` inserted within `self` at `start_time`.

        Args:
            start_time: time to be inserted
            schedule: schedule to be inserted
        """
    return ops.insert(self, start_time, schedule)