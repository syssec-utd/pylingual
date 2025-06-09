def acos(wave):
    """
    Return the arc cosine of a waveform's dependent variable vector.

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.acos

    :raises:
     * RuntimeError (Argument \\`wave\\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(ValueError, 'Math domain error', bool(min(wave._dep_vector) < -1 or max(wave._dep_vector) > 1))
    return _operation(wave, 'acos', 'rad', np.arccos)