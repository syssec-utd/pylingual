def wint(wave):
    """
    Convert a waveform's dependent variable vector to integer.

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.wint

    :raises:
     * RuntimeError (Argument \\`wave\\` is not valid)

     * TypeError (Cannot convert complex to integer)

    .. [[[end]]]
    """
    pexdoc.exh.addex(TypeError, 'Cannot convert complex to integer', wave._dep_vector.dtype.name.startswith('complex'))
    ret = copy.copy(wave)
    ret._dep_vector = ret._dep_vector.astype(np.int)
    return ret