def resolve_inputs(self, layers):
    """Resolve the names of inputs for this layer into shape tuples.

        Parameters
        ----------
        layers : list of :class:`Layer`
            A list of the layers that are available for resolving inputs.

        Raises
        ------
        theanets.util.ConfigurationError :
            If an input cannot be resolved.
        """
    resolved = {}
    for (name, shape) in self._input_shapes.items():
        if shape is None:
            (name, shape) = self._resolve_shape(name, layers)
        resolved[name] = shape
    self._input_shapes = resolved