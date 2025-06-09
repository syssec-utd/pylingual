def _add_sample_measure(self, measure_params, num_samples):
    """Generate memory samples from current statevector.

        Args:
            measure_params (list): List of (qubit, cmembit) values for
                                   measure instructions to sample.
            num_samples (int): The number of memory samples to generate.

        Returns:
            list: A list of memory values in hex format.
        """
    measured_qubits = list({qubit for qubit, cmembit in measure_params})
    num_measured = len(measured_qubits)
    axis = list(range(self._number_of_qubits))
    for qubit in reversed(measured_qubits):
        axis.remove(self._number_of_qubits - 1 - qubit)
    probabilities = np.reshape(np.sum(np.abs(self._statevector) ** 2, axis=tuple(axis)), 2 ** num_measured)
    samples = self._local_random.choice(range(2 ** num_measured), num_samples, p=probabilities)
    memory = []
    for sample in samples:
        classical_memory = self._classical_memory
        for count, (qubit, cmembit) in enumerate(sorted(measure_params)):
            qubit_outcome = int((sample & 1 << count) >> count)
            membit = 1 << cmembit
            classical_memory = classical_memory & ~membit | qubit_outcome << cmembit
        value = bin(classical_memory)[2:]
        memory.append(hex(int(value, 2)))
    return memory