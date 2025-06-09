from typing import List, Optional
import pydantic
from typing_extensions import Literal
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.standard_gates.standard_angle_metaclass import MyMetaAngledClassModel
'\nTo add new standard gates, refer to the following guide\nhttps://docs.google.com/document/d/1Nt9frxnPkSn8swNpOQ983E95eaEiDWaiuWAKglGtUAA/edit#heading=h.e9g9309bzkxt\n'
_POSSIBLE_PARAMETERS: List[str] = ['theta', 'phi', 'lam']
DEFAULT_STANDARD_GATE_ARG_NAME: str = 'TARGET'

class _StandardGate(FunctionParams, metaclass=MyMetaAngledClassModel):
    _name: str = ''
    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=1)
    num_ctrl_qubits: pydantic.NonNegativeInt = pydantic.Field(default=0)

    def _create_ios(self) -> None:
        argument = RegisterUserInput(name=DEFAULT_STANDARD_GATE_ARG_NAME, size=self._num_target_qubits)
        self._inputs = {DEFAULT_STANDARD_GATE_ARG_NAME: argument}
        self._outputs = {DEFAULT_STANDARD_GATE_ARG_NAME: argument}

    @property
    def name(self) -> str:
        return self._name or self.__class__.__name__[:-4].lower()

    @property
    def num_target_qubits(self) -> int:
        return self._num_target_qubits

    def __init_subclass__(cls, angles: Optional[List[str]]=None, **kwargs) -> None:
        super().__init_subclass__()

class UncontrolledStandardGate(_StandardGate):
    num_ctrl_qubits: Literal[0] = pydantic.Field(default=0)

class XGate(UncontrolledStandardGate):
    """
    creates a X gate
    """

    def get_power_order(self) -> int:
        return 2

class YGate(UncontrolledStandardGate):
    """
    creates a Y gate
    """

    def get_power_order(self) -> int:
        return 2

class ZGate(UncontrolledStandardGate):
    """
    create a Z gate
    """

    def get_power_order(self) -> int:
        return 2

class HGate(UncontrolledStandardGate):
    """
    creates a Hadamard gate
    """

    def get_power_order(self) -> int:
        return 2

class IGate(UncontrolledStandardGate):
    """
    creates the identity gate
    """
    _name: str = 'id'

    def get_power_order(self) -> int:
        return 1

class SGate(UncontrolledStandardGate):
    """
    Z**0.5
    """

    def get_power_order(self) -> int:
        return 4

class SdgGate(UncontrolledStandardGate):
    """
    creates the inverse S gate
    """

    def get_power_order(self) -> int:
        return 4

class SXGate(UncontrolledStandardGate):
    """
    X**0.5
    """

    def get_power_order(self) -> int:
        return 4

class SXdgGate(UncontrolledStandardGate):
    """
    creates the inverse SX gate
    """

    def get_power_order(self) -> int:
        return 4

class TGate(UncontrolledStandardGate):
    """
    Z**0.25
    """

    def get_power_order(self) -> int:
        return 8

class TdgGate(UncontrolledStandardGate):
    """
    creates the inverse T gate
    """

    def get_power_order(self) -> int:
        return 8

class SwapGate(UncontrolledStandardGate):
    """
    Swaps between two qubit states
    """
    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)

    def get_power_order(self) -> int:
        return 2

class iSwapGate(UncontrolledStandardGate):
    """
    Swaps between two qubit states and add phase of i to the amplitudes of |01> and |10>
    """
    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)

    def get_power_order(self) -> int:
        return 4