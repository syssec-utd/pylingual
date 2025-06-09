def transpile(circuits, backend=None, basis_gates=None, coupling_map=None, backend_properties=None, initial_layout=None, seed_transpiler=None, optimization_level=None, pass_manager=None, seed_mapper=None):
    """transpile one or more circuits, according to some desired
    transpilation targets.

    All arguments may be given as either singleton or list. In case of list,
    the length must be equal to the number of circuits being transpiled.

    Transpilation is done in parallel using multiprocessing.

    Args:
        circuits (QuantumCircuit or list[QuantumCircuit]):
            Circuit(s) to transpile

        backend (BaseBackend):
            If set, transpiler options are automatically grabbed from
            backend.configuration() and backend.properties().
            If any other option is explicitly set (e.g. coupling_map), it
            will override the backend's.
            Note: the backend arg is purely for convenience. The resulting
                circuit may be run on any backend as long as it is compatible.

        basis_gates (list[str]):
            List of basis gate names to unroll to.
            e.g:
                ['u1', 'u2', 'u3', 'cx']
            If None, do not unroll.

        coupling_map (CouplingMap or list):
            Coupling map (perhaps custom) to target in mapping.
            Multiple formats are supported:
            a. CouplingMap instance

            b. list
                Must be given as an adjacency matrix, where each entry
                specifies all two-qubit interactions supported by backend
                e.g:
                    [[0, 1], [0, 3], [1, 2], [1, 5], [2, 5], [4, 1], [5, 3]]

        backend_properties (BackendProperties):
            properties returned by a backend, including information on gate
            errors, readout errors, qubit coherence times, etc. For a backend
            that provides this information, it can be obtained with:
            ``backend.properties()``

        initial_layout (Layout or dict or list):
            Initial position of virtual qubits on physical qubits.
            If this layout makes the circuit compatible with the coupling_map
            constraints, it will be used.
            The final layout is not guaranteed to be the same, as the transpiler
            may permute qubits through swaps or other means.

            Multiple formats are supported:
            a. Layout instance

            b. dict
                virtual to physical:
                    {qr[0]: 0,
                     qr[1]: 3,
                     qr[2]: 5}

                physical to virtual:
                    {0: qr[0],
                     3: qr[1],
                     5: qr[2]}

            c. list
                virtual to physical:
                    [0, 3, 5]  # virtual qubits are ordered (in addition to named)

                physical to virtual:
                    [qr[0], None, None, qr[1], None, qr[2]]

        seed_transpiler (int):
            sets random seed for the stochastic parts of the transpiler

        optimization_level (int):
            How much optimization to perform on the circuits.
            Higher levels generate more optimized circuits,
            at the expense of longer transpilation time.
                0: no optimization
                1: light optimization
                2: heavy optimization

        pass_manager (PassManager):
            The pass manager to use for a custom pipeline of transpiler passes.
            If this arg is present, all other args will be ignored and the
            pass manager will be used directly (Qiskit will not attempt to
            auto-select a pass manager based on transpile options).

        seed_mapper (int):
            DEPRECATED in 0.8: use ``seed_transpiler`` kwarg instead

    Returns:
        QuantumCircuit or list[QuantumCircuit]: transpiled circuit(s).

    Raises:
        TranspilerError: in case of bad inputs to transpiler or errors in passes
    """
    if seed_mapper:
        warnings.warn('seed_mapper has been deprecated and will be removed in the 0.9 release. Instead use seed_transpiler to set the seed for all stochastic parts of the.', DeprecationWarning)
        seed_transpiler = seed_mapper
    if isinstance(circuits, Schedule) or (isinstance(circuits, list) and all((isinstance(c, Schedule) for c in circuits))):
        return circuits
    circuits = circuits if isinstance(circuits, list) else [circuits]
    transpile_configs = _parse_transpile_args(circuits, backend, basis_gates, coupling_map, backend_properties, initial_layout, seed_transpiler, optimization_level, pass_manager)
    circuits = parallel_map(_transpile_circuit, list(zip(circuits, transpile_configs)))
    if len(circuits) == 1:
        return circuits[0]
    return circuits