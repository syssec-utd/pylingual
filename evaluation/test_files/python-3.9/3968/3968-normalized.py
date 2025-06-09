def compose(self, other, qargs=None, front=False):
    """Return the composition channel self∘other.

        Args:
            other (QuantumChannel): a quantum channel subclass.
            qargs (list): a list of subsystem positions to compose other on.
            front (bool): If False compose in standard order other(self(input))
                          otherwise compose in reverse order self(other(input))
                          [default: False]

        Returns:
            Stinespring: The composition channel as a Stinespring object.

        Raises:
            QiskitError: if other cannot be converted to a channel or
            has incompatible dimensions.
        """
    if qargs is not None:
        return Stinespring(SuperOp(self).compose(other, qargs=qargs, front=front))
    if not isinstance(other, Kraus):
        other = Kraus(other)
    if front and self._input_dim != other._output_dim:
        raise QiskitError('input_dim of self must match output_dim of other')
    if not front and self._output_dim != other._input_dim:
        raise QiskitError('input_dim of other must match output_dim of self')
    return Stinespring(Kraus(self).compose(other, front=front))