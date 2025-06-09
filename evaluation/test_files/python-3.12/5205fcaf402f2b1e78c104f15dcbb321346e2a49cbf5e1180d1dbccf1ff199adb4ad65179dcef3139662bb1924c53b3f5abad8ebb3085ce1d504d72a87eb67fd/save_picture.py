from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin
from .file_name import file_name

class save_picture(Command):
    """
    'save_picture' command.
    
    Parameters
    ----------
        file_name : str
            'file_name' child.
    
    """
    fluent_name = 'save-picture'
    argument_names = ['file_name']
    file_name: file_name = file_name
    '\n    file_name argument of save_picture.\n    '