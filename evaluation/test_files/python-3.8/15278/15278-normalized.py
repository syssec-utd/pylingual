def merge(self, status: 'Status[Input, Output]') -> 'Status[Input, Output]':
    """Merge the failure message from another status into this one.

        Whichever status represents parsing that has gone the farthest is
        retained. If both statuses have gone the same distance, then the
        expected values from both are retained.

        Args:
            status: The status to merge into this one.

        Returns:
            This ``Status`` which may have ``farthest`` and ``expected``
            updated accordingly.
        """
    if status is None or status.farthest is None:
        pass
    elif self.farthest is None:
        self.farthest = status.farthest
        self.expected = status.expected
    elif status.farthest.position < self.farthest.position:
        pass
    elif status.farthest.position > self.farthest.position:
        self.farthest = status.farthest
        self.expected = status.expected
    else:
        self.expected = status.expected + self.expected
    return self