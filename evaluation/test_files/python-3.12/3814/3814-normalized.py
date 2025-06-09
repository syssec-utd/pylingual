def _to_stinespring(rep, data, input_dim, output_dim):
    """Transform a QuantumChannel to the Stinespring representation."""
    if rep == 'Stinespring':
        return data
    if rep == 'Operator':
        return _from_operator('Stinespring', data, input_dim, output_dim)
    if rep != 'Kraus':
        data = _to_kraus(rep, data, input_dim, output_dim)
    return _kraus_to_stinespring(data, input_dim, output_dim)