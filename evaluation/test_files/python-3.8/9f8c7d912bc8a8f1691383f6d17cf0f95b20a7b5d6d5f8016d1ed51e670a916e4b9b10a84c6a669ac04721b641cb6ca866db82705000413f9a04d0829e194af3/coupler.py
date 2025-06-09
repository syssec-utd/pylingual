from SiPANN.scee import Standard

def coupler(width: float=0.5, thickness: float=0.22, gap: float=0.22, length: float=10.0, sw_angle: float=90.0, dx: float=1.5, dy: float=5.0, **kwargs):
    """Return simphony Directional coupler model.

    Args:
        width: Width of the straight in um (Valid for 0.4-0.6)
        thickness: Thickness of straight in um (Valid for 0.18-0.24)
        gap: Minimum distance between the two straights edge in um. (Must be > 0.1)
        length: float or ndarray Length of the straight portion of both straights in um.
        dx: Horizontal distance between end of coupler until straight portion in nm.
        dy: Vertical distance between end of coupler until straight portion in um.
        sw_angle: Sidewall angle from horizontal in degrees
        kwargs: geometrical args that this model ignores

    This is what most people think of when they think directional coupler.
    Ports are named as

    .. code::

                                                   H
               dx                                 dx
            |------|                           |------|
          2 ________                           _______ 4       _ _
                    \\                         /           |     |
                     \\        length         /            |    _|_V
                      ======================= gap         | dy
                     /                       \\            |
            ________/                         \\_______    |
          1                                            3



    """
    width *= 1000.0
    thickness *= 1000.0
    gap *= 1000.0
    length *= 1000.0
    H = dx * 1000.0
    V = dy * 1000.0 / 2
    return Standard(width=width, thickness=thickness, gap=gap, length=length, H=H, V=V, sw_angle=sw_angle)
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    c = coupler()
    wavelength = np.linspace(1500, 1600, 500)
    k = c.predict((1, 4), wavelength)
    t = c.predict((1, 3), wavelength)
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plt.plot(wavelength, np.abs(k) ** 2, label='k')
    plt.plot(wavelength, np.abs(t) ** 2, label='t')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Magnitude Squared')
    plt.title('Crossover at $\\lambda \\approx 1550nm$')
    plt.legend()
    plt.show()