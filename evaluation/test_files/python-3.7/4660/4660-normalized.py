def clear(self):
    """
        Reset the current HyperLogLog to empty.
        """
    self.reg = np.zeros((self.m,), dtype=np.int8)