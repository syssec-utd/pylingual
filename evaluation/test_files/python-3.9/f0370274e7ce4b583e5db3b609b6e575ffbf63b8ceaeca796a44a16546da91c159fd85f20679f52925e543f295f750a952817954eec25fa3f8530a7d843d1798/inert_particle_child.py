from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .density_3 import density
from .specific_heat_2 import specific_heat
from .thermal_conductivity_3 import thermal_conductivity
from .thermophoretic_co import thermophoretic_co
from .scattering_factor import scattering_factor
from .emissivity import emissivity
from .viscosity_2 import viscosity
from .dpm_surften import dpm_surften
from .electric_conductivity_1 import electric_conductivity
from .dual_electric_conductivity_1 import dual_electric_conductivity
from .magnetic_permeability import magnetic_permeability
from .charge_density import charge_density

class inert_particle_child(Group):
    """
    'child_object_type' of inert_particle.
    """
    fluent_name = 'child-object-type'
    child_names = ['density', 'specific_heat', 'thermal_conductivity', 'thermophoretic_co', 'scattering_factor', 'emissivity', 'viscosity', 'dpm_surften', 'electric_conductivity', 'dual_electric_conductivity', 'magnetic_permeability', 'charge_density']
    density: density = density
    '\n    density child of inert_particle_child.\n    '
    specific_heat: specific_heat = specific_heat
    '\n    specific_heat child of inert_particle_child.\n    '
    thermal_conductivity: thermal_conductivity = thermal_conductivity
    '\n    thermal_conductivity child of inert_particle_child.\n    '
    thermophoretic_co: thermophoretic_co = thermophoretic_co
    '\n    thermophoretic_co child of inert_particle_child.\n    '
    scattering_factor: scattering_factor = scattering_factor
    '\n    scattering_factor child of inert_particle_child.\n    '
    emissivity: emissivity = emissivity
    '\n    emissivity child of inert_particle_child.\n    '
    viscosity: viscosity = viscosity
    '\n    viscosity child of inert_particle_child.\n    '
    dpm_surften: dpm_surften = dpm_surften
    '\n    dpm_surften child of inert_particle_child.\n    '
    electric_conductivity: electric_conductivity = electric_conductivity
    '\n    electric_conductivity child of inert_particle_child.\n    '
    dual_electric_conductivity: dual_electric_conductivity = dual_electric_conductivity
    '\n    dual_electric_conductivity child of inert_particle_child.\n    '
    magnetic_permeability: magnetic_permeability = magnetic_permeability
    '\n    magnetic_permeability child of inert_particle_child.\n    '
    charge_density: charge_density = charge_density
    '\n    charge_density child of inert_particle_child.\n    '