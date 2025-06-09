from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .option_2 import option
from .value import value
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf

class t(Group):
    """
    't' child.
    """
    fluent_name = 't'
    child_names = ['option', 'value', 'profile_name', 'field_name', 'udf']
    option: option = option
    '\n    option child of t.\n    '
    value: value = value
    '\n    value child of t.\n    '
    profile_name: profile_name = profile_name
    '\n    profile_name child of t.\n    '
    field_name: field_name = field_name
    '\n    field_name child of t.\n    '
    udf: udf = udf
    '\n    udf child of t.\n    '