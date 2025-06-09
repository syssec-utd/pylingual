def drag(duration: int, amp: complex, sigma: float, beta: float, name: str=None) -> SamplePulse:
    """Generates Y-only correction DRAG `SamplePulse` for standard nonlinear oscillator (SNO) [1].

    Centered at `duration/2` and zeroed at `t=-1` to prevent large initial discontinuity.

    Applies `left` sampling strategy to generate discrete pulse from continuous function.

    [1] Gambetta, J. M., Motzoi, F., Merkel, S. T. & Wilhelm, F. K.
        Analytic control methods for high-fidelity unitary operations
        in a weakly nonlinear oscillator. Phys. Rev. A 83, 012308 (2011).


    Args:
        duration: Duration of pulse. Must be greater than zero.
        amp: Pulse amplitude at `center`.
        sigma: Width (standard deviation) of pulse.
        beta: Y correction amplitude. For the SNO this is $\\beta=-\\frac{\\lambda_1^2}{4\\Delta_2}$.
            Where $\\lambds_1$ is the relative coupling strength between the first excited and second
            excited states and $\\Delta_2$ is the detuning between the resepective excited states.
        name: Name of pulse.
    """
    center = duration / 2
    zeroed_width = duration + 2
    return _sampled_drag_pulse(duration, amp, center, sigma, beta, zeroed_width=zeroed_width, rescale_amp=True, name=name)