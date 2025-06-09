from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .expression_child import expression_child

class expression(NamedObject[expression_child], _CreatableNamedObjectMixin[expression_child]):
    """
    'expression' child.
    """
    fluent_name = 'expression'
    child_object_type: expression_child = expression_child
    '\n    child_object_type of expression.\n    '