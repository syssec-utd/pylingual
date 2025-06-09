def obj_overhead(self):
    """Returns all objects that are considered a profiler overhead.
        Objects are hardcoded for convenience.
        """
    overhead = [self, self._resulting_events, self._events_list, self._process]
    overhead_count = _get_object_count_by_type(overhead)
    overhead_count[dict] += 2
    return overhead_count