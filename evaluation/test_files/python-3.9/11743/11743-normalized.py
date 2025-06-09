def fracpols(str, **kwargs):
    """Output fractional linear and circular polarizations for a
    rawspec cross polarization .fil file. NOT STANDARD USE"""
    (I, Q, U, V, L) = get_stokes(str, **kwargs)
    return (L / I, V / I)