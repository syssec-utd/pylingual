from abaqusConstants import *
from .BoundaryConditionState import BoundaryConditionState

class ConnDisplacementBCState(BoundaryConditionState):
    """The ConnDisplacementBCState object stores the propagating data for a connector
    displacement/rotation boundary condition in a step. One instance of this object is
    created internally by the ConnDisplacementBC object for each step. The instance is also
    deleted internally by the ConnDisplacementBC object.
    The ConnDisplacementBCState object has no constructor or methods.
    The ConnDisplacementBCState object is derived from the BoundaryConditionState object.

    .. note:: 
        This object can be accessed by:

        .. code-block:: python

            import load
            mdb.models[name].steps[name].boundaryConditionStates[name]

        The corresponding analysis keywords are:

        - CONNECTOR MOTION
    """
    u1: float = None
    u2: float = None
    u3: float = None
    ur1: float = None
    ur2: float = None
    ur3: float = None
    u1State: SymbolicConstant = None
    u2State: SymbolicConstant = None
    u3State: SymbolicConstant = None
    ur1State: SymbolicConstant = None
    ur2State: SymbolicConstant = None
    ur3State: SymbolicConstant = None
    amplitudeState: SymbolicConstant = None
    status: SymbolicConstant = None
    amplitude: str = ''