def disable(self):
    """
        Disables interceptors and stops intercepting any outgoing HTTP traffic.
        """
    if not self.active:
        return None
    self.mock_engine.disable()
    self.active = False