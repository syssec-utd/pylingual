from SiPANN.scee import HalfRacetrack

def coupler_ring(radius: float=5.0, width: float=0.5, thickness: float=0.22, gap: float=0.22, length_x: float=4.0, sw_angle: float=90.0, **kwargs):
    """Return model for for half a ring coupler.

    Args:
        radius: 5
        width: width um (Valid for 0.4-0.6)
        thickness: Thickness in um (Valid for 0.18-0.24)
        gap: distance between straights in um. (Must be > 0.1)
        length_x: Length of straight portion of coupler in um
        sw_angle: Sidewall angle from horizontal in degrees
        kwargs: geometrical args that this model ignores

    .. code::

        pin naming in sipann

            2 \\           / 4
               \\         /
                ---------
            1---------------3

        for simphony/gdsfactory

           o2            o3
           |             |
            \\           /
             \\         /
           ---=========---
        o1    length_x    o4


    """
    width *= 1000.0
    thickness *= 1000.0
    gap *= 1000.0
    length = length_x * 1000.0
    radius *= 1000.0
    return HalfRacetrack(radius=radius, width=width, thickness=thickness, gap=gap, length=length, sw_angle=sw_angle)
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    c = coupler_ring()
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