def gates_to_uncompute(self):
    """
        Call to create a circuit with gates that take the
        desired vector to zero.

        Returns:
            QuantumCircuit: circuit to take self.params vector to |00..0>
        """
    q = QuantumRegister(self.num_qubits)
    circuit = QuantumCircuit(q, name='disentangler')
    remaining_param = self.params
    for i in range(self.num_qubits):
        remaining_param, thetas, phis = Initialize._rotations_to_disentangle(remaining_param)
        rz_mult = self._multiplex(RZGate, phis)
        ry_mult = self._multiplex(RYGate, thetas)
        circuit.append(rz_mult.to_instruction(), q[i:self.num_qubits])
        circuit.append(ry_mult.to_instruction(), q[i:self.num_qubits])
    return circuit