def iffti(wave, npoints=None, indep_min=None, indep_max=None):
    """
    Return the imaginary part of the inverse Fast Fourier Transform of a waveform.

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.iffti

    :raises:
     * RuntimeError (Argument \\`indep_max\\` is not valid)

     * RuntimeError (Argument \\`indep_min\\` is not valid)

     * RuntimeError (Argument \\`npoints\\` is not valid)

     * RuntimeError (Argument \\`wave\\` is not valid)

     * RuntimeError (Incongruent \\`indep_min\\` and \\`indep_max\\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    return imag(ifft(wave, npoints, indep_min, indep_max))