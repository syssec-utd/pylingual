from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .solve_tke import solve_tke
from .wall_echo import wall_echo

class reynolds_stress_options(Group):
    """
    'reynolds_stress_options' child.
    """
    fluent_name = 'reynolds-stress-options'
    child_names = ['solve_tke', 'wall_echo']
    solve_tke: solve_tke = solve_tke
    '\n    solve_tke child of reynolds_stress_options.\n    '
    wall_echo: wall_echo = wall_echo
    '\n    wall_echo child of reynolds_stress_options.\n    '