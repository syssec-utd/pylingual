def register_updates(self, *updates):
    """
        Register updates that will be executed in each iteration.
        """
    for key, node in updates:
        if key not in self._registered_updates:
            self.updates.append((key, node))
            self._registered_updates.add(key)