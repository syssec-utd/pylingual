from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .child_object_type_child_1 import child_object_type_child

class tss_scalar(NamedObject[child_object_type_child], _NonCreatableNamedObjectMixin[child_object_type_child]):
    """
    'tss_scalar' child.
    """
    fluent_name = 'tss-scalar'
    child_object_type: child_object_type_child = child_object_type_child
    '\n    child_object_type of tss_scalar.\n    '