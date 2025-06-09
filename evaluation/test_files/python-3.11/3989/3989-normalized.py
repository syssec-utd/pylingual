def update_x(self, x, indices=None):
    """
        Update partial or entire x.

        Args:
            x (numpy.ndarray or list): to-be-updated x
            indices (numpy.ndarray or list or optional): to-be-updated qubit indices

        Returns:
            Pauli: self

        Raises:
            QiskitError: when updating whole x, the number of qubits must be the same.
        """
    x = _make_np_bool(x)
    if indices is None:
        if len(self._x) != len(x):
            raise QiskitError('During updating whole x, you can not change the number of qubits.')
        self._x = x
    else:
        if not isinstance(indices, list) and (not isinstance(indices, np.ndarray)):
            indices = [indices]
        for p, idx in enumerate(indices):
            self._x[idx] = x[p]
    return self