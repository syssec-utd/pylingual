from dataclasses import dataclass
from typing import Optional
from telebox.errors import TeleboxError
from telebox.state_machine.state import State
from telebox.dispatcher.handlers.handlers.event import AbstractEventHandler

@dataclass
class StateMachineError(TeleboxError):
    pass

@dataclass
class StateExistsError(StateMachineError):
    state: State

@dataclass
class StateNameExistsError(StateMachineError):
    state_name: str

@dataclass
class TransitionExistsError(StateMachineError):
    source_state: State
    handler: AbstractEventHandler
    direction: Optional[str] = None

@dataclass
class DestinationStateNotFoundError(StateMachineError):
    source_state: State
    handler: AbstractEventHandler
    direction: Optional[str] = None

@dataclass
class NextStateNotFoundError(StateMachineError):
    source_state: State
    handler: AbstractEventHandler
    direction: Optional[str] = None

@dataclass
class PreviousStateNotFoundError(StateMachineError):
    current_state: State

@dataclass
class StateNotFoundError(StateMachineError):
    state_name: str