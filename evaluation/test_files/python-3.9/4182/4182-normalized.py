def create_tomography_circuits(circuit, qreg, creg, tomoset):
    """
    Add tomography measurement circuits to a QuantumProgram.

    The quantum program must contain a circuit 'name', which is treated as a
    state preparation circuit for state tomography, or as teh circuit being
    measured for process tomography. This function then appends the circuit
    with a set of measurements specified by the input `tomography_set`,
    optionally it also prepends the circuit with state preparation circuits if
    they are specified in the `tomography_set`.

    For n-qubit tomography with a tomographically complete set of preparations
    and measurements this results in $4^n 3^n$ circuits being added to the
    quantum program.

    Args:
        circuit (QuantumCircuit): The circuit to be appended with tomography
                                  state preparation and/or measurements.
        qreg (QuantumRegister): the quantum register containing qubits to be
                                measured.
        creg (ClassicalRegister): the classical register containing bits to
                                  store measurement outcomes.
        tomoset (tomography_set): the dict of tomography configurations.

    Returns:
        list: A list of quantum tomography circuits for the input circuit.

    Raises:
        QiskitError: if circuit is not a valid QuantumCircuit

    Example:
        For a tomography set specifying state tomography of qubit-0 prepared
        by a circuit 'circ' this would return:
        ```
        ['circ_meas_X(0)', 'circ_meas_Y(0)', 'circ_meas_Z(0)']
        ```
        For process tomography of the same circuit with preparation in the
        SIC-POVM basis it would return:
        ```
        [
            'circ_prep_S0(0)_meas_X(0)', 'circ_prep_S0(0)_meas_Y(0)',
            'circ_prep_S0(0)_meas_Z(0)', 'circ_prep_S1(0)_meas_X(0)',
            'circ_prep_S1(0)_meas_Y(0)', 'circ_prep_S1(0)_meas_Z(0)',
            'circ_prep_S2(0)_meas_X(0)', 'circ_prep_S2(0)_meas_Y(0)',
            'circ_prep_S2(0)_meas_Z(0)', 'circ_prep_S3(0)_meas_X(0)',
            'circ_prep_S3(0)_meas_Y(0)', 'circ_prep_S3(0)_meas_Z(0)'
        ]
        ```
    """
    if not isinstance(circuit, QuantumCircuit):
        raise QiskitError('Input circuit must be a QuantumCircuit object')
    dics = tomoset['circuits']
    labels = tomography_circuit_names(tomoset, circuit.name)
    tomography_circuits = []
    for (label, conf) in zip(labels, dics):
        tmp = circuit
        if 'prep' in conf:
            prep = QuantumCircuit(qreg, creg, name='tmp_prep')
            for (qubit, op) in conf['prep'].items():
                tomoset['prep_basis'].prep_gate(prep, qreg[qubit], op)
                prep.barrier(qreg[qubit])
            tmp = prep + tmp
        meas = QuantumCircuit(qreg, creg, name='tmp_meas')
        for (qubit, op) in conf['meas'].items():
            meas.barrier(qreg[qubit])
            tomoset['meas_basis'].meas_gate(meas, qreg[qubit], op)
            meas.measure(qreg[qubit], creg[qubit])
        tmp = tmp + meas
        tmp.name = label
        tomography_circuits.append(tmp)
    logger.info('>> created tomography circuits for "%s"', circuit.name)
    return tomography_circuits