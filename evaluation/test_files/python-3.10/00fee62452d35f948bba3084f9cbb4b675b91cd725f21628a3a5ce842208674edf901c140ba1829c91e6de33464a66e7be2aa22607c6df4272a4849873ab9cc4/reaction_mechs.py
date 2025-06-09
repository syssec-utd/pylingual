from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .option_9 import option

class reaction_mechs(Group):
    """
    'reaction_mechs' child.
    """
    fluent_name = 'reaction-mechs'
    child_names = ['option']
    option: option = option
    '\n    option child of reaction_mechs.\n    '