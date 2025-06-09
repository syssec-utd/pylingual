def remove_chain(self, name):
    """
        Remove chain from current shelve file

        Args:
            name: chain name
        """
    if name in self.chains:
        delattr(self.chains, name)
    else:
        raise ValueError('Chain with this name not found')