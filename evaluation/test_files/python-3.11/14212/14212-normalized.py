def find(self, which, param):
    """Get a parameter from a layer in the network.

        Parameters
        ----------
        which : int or str
            The layer that owns the parameter to return.

            If this is an integer, then 0 refers to the input layer, 1 refers
            to the first hidden layer, 2 to the second, and so on.

            If this is a string, the layer with the corresponding name, if any,
            will be used.

        param : int or str
            Name of the parameter to retrieve from the specified layer, or its
            index in the parameter list of the layer.

        Raises
        ------
        KeyError
            If there is no such layer, or if there is no such parameter in the
            specified layer.

        Returns
        -------
        param : Theano shared variable
            A shared parameter variable from the indicated layer.
        """
    for i, layer in enumerate(self.layers):
        if which == i or which == layer.name:
            return layer.find(param)
    raise KeyError(which)