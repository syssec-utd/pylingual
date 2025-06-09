def multiple_l2_norm(tensors):
    """
    Get the L2 norm of multiple tensors.
    This function is taken from blocks.
    """
    flattened = [T.as_tensor_variable(t).flatten() for t in tensors]
    flattened = [t if t.ndim > 0 else t.dimshuffle('x') for t in flattened]
    joined = T.join(0, *flattened)
    return T.sqrt(T.sqr(joined).sum())