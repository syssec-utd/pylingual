def updates(self, **kwargs):
    """Return expressions to run as updates during network training.

        Returns
        -------
        updates : list of (parameter, expression) pairs
            A list of named parameter update expressions for this network.
        """
    regs = regularizers.from_kwargs(self, **kwargs)
    (_, updates) = self.build_graph(regs)
    return updates