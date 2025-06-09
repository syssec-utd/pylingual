from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .option_8 import option
from .value import value

class youngs_modulus_1(Group):
    """
    'youngs_modulus_1' child.
    """
    fluent_name = 'youngs-modulus-1'
    child_names = ['option', 'value']
    option: option = option
    '\n    option child of youngs_modulus_1.\n    '
    value: value = value
    '\n    value child of youngs_modulus_1.\n    '