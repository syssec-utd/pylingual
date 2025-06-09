def add_bias(self, name, size, mean=0, std=1):
    """Helper method to create a new bias vector.

        Parameters
        ----------
        name : str
            Name of the parameter to add.
        size : int
            Size of the bias vector.
        mean : float, optional
            Mean value for randomly-initialized biases. Defaults to 0.
        std : float, optional
            Standard deviation for randomly-initialized biases. Defaults to 1.
        """
    mean = self.kwargs.get('mean_{}'.format(name), mean)
    std = self.kwargs.get('std_{}'.format(name), std)
    self._params.append(theano.shared(util.random_vector(size, mean, std, rng=self.rng), name=self._fmt(name)))