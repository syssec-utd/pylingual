def decompose(self):
    """Call a decomposition pass on this circuit,
        to decompose one level (shallow decompose).

        Returns:
            QuantumCircuit: a circuit one level decomposed
        """
    from qiskit.transpiler.passes.decompose import Decompose
    from qiskit.converters.circuit_to_dag import circuit_to_dag
    from qiskit.converters.dag_to_circuit import dag_to_circuit
    pass_ = Decompose()
    decomposed_dag = pass_.run(circuit_to_dag(self))
    return dag_to_circuit(decomposed_dag)