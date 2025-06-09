def add_event(self, event):
    """Adds events to the queue. Will ignore events that occur before the
        settle time for that pin/direction. Such events are assumed to be
        bouncing.
        """
    for pin_function_map in self.pin_function_maps:
        if _event_matches_pin_function_map(event, pin_function_map):
            pin_settle_time = pin_function_map.settle_time
            break
    else:
        return
    threshold_time = self.last_event_time[event.pin_num] + pin_settle_time
    if event.timestamp > threshold_time:
        self.put(event)
        self.last_event_time[event.pin_num] = event.timestamp