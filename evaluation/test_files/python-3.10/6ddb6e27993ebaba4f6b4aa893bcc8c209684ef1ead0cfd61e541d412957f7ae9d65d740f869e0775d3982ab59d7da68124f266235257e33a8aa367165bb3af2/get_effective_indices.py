"""Calculate the effective refractive index for a 1D mode."""
from typing import List
import numpy as np
from scipy.optimize import fsolve
from typing_extensions import Literal

def get_effective_indices(ncore: float, nsubstrate: float, ncladding: float, thickness: float, wavelength: float, polarization: Literal['te', 'tm']) -> List[float]:
    """Returns the effective refractive indices for a 1D mode.

    Args:
        epsilon_core: Relative permittivity of the film.
        epsilon_substrate: Relative permittivity of the substrate.
        epsilon_cladding: Relative permittivity of the cladding.
        thickness: Thickness of the film in um.
        wavelength: Wavelength in um.
        polarization: Either "te" or "tm".

    .. code::

        -----------------      |
        ncladding             inf
        -----------------      |
        ncore              thickness
        -----------------      |
        nsubstrate            inf
        -----------------      |

    .. code::

        import gdsfactory.simulation as sim

        neffs = sim.get_effective_indices(
            ncore=3.4777,
            ncladding=1.444,
            nsubstrate=1.444,
            thickness=0.22,
            wavelength=1.55,
            polarization="te",
        )

    """
    epsilon_core = ncore ** 2
    epsilon_cladding = ncladding ** 2
    epsilon_substrate = nsubstrate ** 2
    thickness = thickness * 1e-06
    wavelength = wavelength * 1e-06
    if polarization == 'te':
        tm = False
    elif polarization == 'tm':
        tm = True
    else:
        raise ValueError('Polarization must be "te" or "tm"')
    k_0 = 2 * np.pi / wavelength

    def k_f(e_eff):
        return k_0 * np.sqrt(epsilon_core - e_eff) / (epsilon_core if tm else 1)

    def k_s(e_eff):
        return k_0 * np.sqrt(e_eff - epsilon_substrate) / (epsilon_substrate if tm else 1)

    def k_c(e_eff):
        return k_0 * np.sqrt(e_eff - epsilon_cladding) / (epsilon_cladding if tm else 1)

    def objective(e_eff):
        return 1 / np.tan(k_f(e_eff) * thickness) - (k_f(e_eff) ** 2 - k_s(e_eff) * k_c(e_eff)) / (k_f(e_eff) * (k_s(e_eff) + k_c(e_eff)))
    x = np.linspace(min(epsilon_substrate, epsilon_cladding) + 1e-10, epsilon_core - 1e-10, 1000)
    indices_temp = x[np.abs(objective(x)) < 0.1]
    if not len(indices_temp):
        return []
    indices_temp = fsolve(objective, indices_temp)
    indices = []
    for index in indices_temp:
        if not any((np.isclose(index, i, atol=1e-05) for i in indices)):
            indices.append(index)
    return np.sqrt(indices).tolist()

def test_effective_index():
    neff = get_effective_indices(ncore=3.4777, ncladding=1.444, nsubstrate=1.444, thickness=0.22, wavelength=1.55, polarization='te')
    assert np.isclose(neff[0], 2.8494636999424405)
if __name__ == '__main__':
    print(get_effective_indices(ncore=3.4777, ncladding=1.444, nsubstrate=1.444, thickness=0.22, wavelength=1.55, polarization='te'))