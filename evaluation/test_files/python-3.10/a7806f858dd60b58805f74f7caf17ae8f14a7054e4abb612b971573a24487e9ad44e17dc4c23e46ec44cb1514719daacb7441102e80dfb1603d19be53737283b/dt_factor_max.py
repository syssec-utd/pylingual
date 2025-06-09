from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

class dt_factor_max(Real):
    """
    Set maximum limit for increase in pseudo time step size.
    """
    fluent_name = 'dt-factor-max'