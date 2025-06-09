""" mobility of particle
"""
import numpy as np
from particula.util.input_handling import in_radius, in_scalar, in_viscosity
from particula.util.slip_correction import scf
from particula.util.dynamic_viscosity import dyn_vis

def pam(radius=None, scf_val=None, vis_val=None, **kwargs):
    """ particle aerodynamic mobility
    """
    rad = in_radius(radius)
    scf_val = in_scalar(scf_val) if scf_val is not None else scf(radius=rad, **kwargs)
    vis_val = in_viscosity(vis_val) if vis_val is not None else dyn_vis(radius=rad, **kwargs)
    return scf_val / (3 * np.pi * vis_val * rad * 2)