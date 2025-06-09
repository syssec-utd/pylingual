from ansys.fluent.core.solver.flobject import *
from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin
from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin
from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

class terminology(Integer):
    """
    Select Rotor Disk Orientation Terminology:
    
     - Enter 0 if using Rotor Disk Angles 
     - Enter 1 if using Rotor Disk Normal 
    
    For more details please consult the help option of the corresponding menu or TUI command.
    """
    fluent_name = 'terminology'