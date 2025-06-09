def add_annotation(self, state_or_vector, text, **kwargs):
    """Add a text or LaTeX annotation to Bloch sphere,
        parametrized by a qubit state or a vector.

        Args:
            state_or_vector (array_like):
                Position for the annotation.
                Qobj of a qubit or a vector of 3 elements.
            text (str):
                Annotation text.
                You can use LaTeX, but remember to use raw string
                e.g. r"$\\langle x \\rangle$"
                or escape backslashes
                e.g. "$\\\\langle x \\\\rangle$".
            **kwargs:
                Options as for mplot3d.axes3d.text, including:
                fontsize, color, horizontalalignment, verticalalignment.
        Raises:
            Exception: If input not array_like or tuple.
        """
    if isinstance(state_or_vector, (list, np.ndarray, tuple)) and len(state_or_vector) == 3:
        vec = state_or_vector
    else:
        raise Exception('Position needs to be specified by a qubit ' + 'state or a 3D vector.')
    self.annotations.append({'position': vec, 'text': text, 'opts': kwargs})