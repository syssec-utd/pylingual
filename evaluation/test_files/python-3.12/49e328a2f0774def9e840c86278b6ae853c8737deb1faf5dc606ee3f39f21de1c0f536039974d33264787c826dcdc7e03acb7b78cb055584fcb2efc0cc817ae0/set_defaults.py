from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .set_defaults_child import set_defaults_child

class set_defaults(NamedObject[set_defaults_child], _CreatableNamedObjectMixin[set_defaults_child]):
    """
    'set_defaults' child.
    """
    fluent_name = 'set-defaults'
    child_object_type: set_defaults_child = set_defaults_child
    '\n    child_object_type of set_defaults.\n    '