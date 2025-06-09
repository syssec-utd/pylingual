def gaussian(times: np.ndarray, amp: complex, center: float, sigma: float, zeroed_width: Union[None, float]=None, rescale_amp: bool=False, ret_x: bool=False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    """Continuous unnormalized gaussian pulse.

    Integrated area under curve is $\\Omega_g(amp, sigma) = amp \\times np.sqrt(2\\pi \\sigma^2)$

    Args:
        times: Times to output pulse for.
        amp: Pulse amplitude at `center`. If `zeroed_width` is set pulse amplitude at center
            will be $amp-\\Omega_g(center\\pm zeroed_width/2)$ unless `rescale_amp` is set,
            in which case all samples will be rescaled such that the center
            amplitude will be `amp`.
        center: Center (mean) of pulse.
        sigma: Width (standard deviation) of pulse.
        zeroed_width: Subtract baseline to gaussian pulses to make sure
                 $\\Omega_g(center \\pm zeroed_width/2)=0$ is satisfied. This is used to avoid
                 large discontinuities at the start of a gaussian pulse.
        rescale_amp: If `zeroed_width` is not `None` and `rescale_amp=True` the pulse will
                     be rescaled so that $\\Omega_g(center)-\\Omega_g(center\\pm zeroed_width/2)=amp$.
        ret_x: Return centered and standard deviation normalized pulse location.
               $x=(times-center)/sigma.
    """
    times = np.asarray(times, dtype=np.complex_)
    x = (times - center) / sigma
    gauss = amp * np.exp(-x ** 2 / 2).astype(np.complex_)
    if zeroed_width is not None:
        gauss = _fix_gaussian_width(gauss, amp=amp, center=center, sigma=sigma, zeroed_width=zeroed_width, rescale_amp=rescale_amp)
    if ret_x:
        return (gauss, x)
    return gauss