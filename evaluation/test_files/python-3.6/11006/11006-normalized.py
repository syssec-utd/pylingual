def _max_of_integrand(t_val, f, g, inverse_time=None, return_log=False):
    """
    Evaluates max_tau f(t+tau)*g(tau) or max_tau f(t-tau)g(tau) if inverse time is TRUE

    Parameters
    -----------

     t_val : double
        Time point

     f : Interpolation object
        First multiplier in convolution

     g : Interpolation object
        Second multiplier in convolution

     inverse_time : bool, None
        time direction. If True, then the f(t-tau)*g(tau) is calculated, otherwise,
        f(t+tau)*g(tau)

     return_log : bool
        If True, the logarithm will be returned


    Returns
    -------

     FG : Distribution
        The function to be integrated as Distribution object (interpolator)

    """
    FG = _convolution_integrand(t_val, f, g, inverse_time, return_log=True)
    if FG == ttconf.BIG_NUMBER:
        res = (ttconf.BIG_NUMBER, 0)
    else:
        X = FG.x[FG.y.argmin()]
        Y = FG.y.min()
        res = (Y, X)
    if not return_log:
        res[0] = np.log(res[0])
    return res