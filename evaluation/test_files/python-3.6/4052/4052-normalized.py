def conjugate(self):
    """Return the conjugate of the operator."""
    return Operator(np.conj(self.data), self.input_dims(), self.output_dims())