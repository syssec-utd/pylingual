def put(self, v):
    """
        Put an unsigned integer into the queue. This method always assumes that there is space in the queue.
        ( In the circular buffer, this is guaranteed by the implementation )
        :param v: The item to insert. Must be >= 0, as -2 is used to signal a queue close.
        :return:
        """
    if v is QueueClosed:
        v = -2
    else:
        assert v >= 0
    with self.cvar:
        assert self.size.value < len(self.vals)
        head = (self.tail.value + self.size.value) % len(self.vals)
        self.vals[head] = v
        self.size.value += 1
        self.cvar.notify()