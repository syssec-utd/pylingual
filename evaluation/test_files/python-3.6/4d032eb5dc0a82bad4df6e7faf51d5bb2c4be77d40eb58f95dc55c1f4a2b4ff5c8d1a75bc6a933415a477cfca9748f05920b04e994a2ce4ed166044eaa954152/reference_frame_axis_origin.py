from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .child_object_type_child import child_object_type_child

class reference_frame_axis_origin(ListObject[child_object_type_child]):
    """
    'reference_frame_axis_origin' child.
    """
    fluent_name = 'reference-frame-axis-origin'
    child_object_type: child_object_type_child = child_object_type_child
    '\n    child_object_type of reference_frame_axis_origin.\n    '