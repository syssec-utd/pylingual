def register_monitors(self, *monitors):
    """
        Register monitors they should be tuple of name and Theano variable.
        """
    for (key, node) in monitors:
        if key not in self._registered_monitors:
            node *= 1.0
            self.training_monitors.append((key, node))
            self.testing_monitors.append((key, node))
            self._registered_monitors.add(key)