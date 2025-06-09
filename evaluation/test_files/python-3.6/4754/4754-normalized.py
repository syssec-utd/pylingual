def set(self, value):
    """
        Set a new value for this thing.

        value -- value to set
        """
    if self.value_forwarder is not None:
        self.value_forwarder(value)
    self.notify_of_external_update(value)