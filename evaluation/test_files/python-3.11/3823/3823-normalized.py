def _stinespring_to_choi(data, input_dim, output_dim):
    """Transform Stinespring representation to Choi representation."""
    trace_dim = data[0].shape[0] // output_dim
    stine_l = np.reshape(data[0], (output_dim, trace_dim, input_dim))
    if data[1] is None:
        stine_r = stine_l
    else:
        stine_r = np.reshape(data[1], (output_dim, trace_dim, input_dim))
    return np.reshape(np.einsum('iAj,kAl->jilk', stine_l, stine_r.conj()), 2 * [input_dim * output_dim])