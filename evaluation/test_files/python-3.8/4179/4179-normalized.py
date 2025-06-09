def __sic_prep_gates(circuit, qreg, op):
    """
    Add state preparation gates to a circuit.
    """
    (bas, proj) = op
    if bas != 'S':
        raise QiskitError('Not in SIC basis!')
    theta = -2 * np.arctan(np.sqrt(2))
    if proj == 1:
        circuit.u3(theta, np.pi, 0.0, qreg)
    elif proj == 2:
        circuit.u3(theta, np.pi / 3, 0.0, qreg)
    elif proj == 3:
        circuit.u3(theta, -np.pi / 3, 0.0, qreg)