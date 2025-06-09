from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf

class wave_spect_min_freq(Group):
    """
    'wave_spect_min_freq' child.
    """
    fluent_name = 'wave-spect-min-freq'
    child_names = ['option', 'constant', 'profile_name', 'field_name', 'udf']
    option: option = option
    '\n    option child of wave_spect_min_freq.\n    '
    constant: constant = constant
    '\n    constant child of wave_spect_min_freq.\n    '
    profile_name: profile_name = profile_name
    '\n    profile_name child of wave_spect_min_freq.\n    '
    field_name: field_name = field_name
    '\n    field_name child of wave_spect_min_freq.\n    '
    udf: udf = udf
    '\n    udf child of wave_spect_min_freq.\n    '