def call_mee(backend=0, *args, **kwargs):
    """
    decide backend and return RCWA mee instance

    Args:
        backend: decide backend. 0 is numpy and 1 is JAX.
        *args: passed to RCWA instance
        **kwargs: passed to RCWA instance

    Returns:
        RCWA: RCWA mee instance

    """
    if backend == 0:
        from .on_numpy.mee import MeeNumpy
        mee = MeeNumpy(*args, backend=backend, **kwargs)
    elif backend == 1:
        from .on_jax.mee import MeeJax
        mee = MeeJax(*args, backend=backend, **kwargs)
    elif backend == 2:
        from .on_torch.mee import MeeTorch
        mee = MeeTorch(*args, backend=backend, **kwargs)
    else:
        raise ValueError
    return mee