from vid2info.utils.config import TIME_FORMAT, ELEMENT_AGE_TIME_FORMAT
from vid2info.utils.general import time_as_str
from vid2info.state.finite_state_machine.config_keys import INITIAL_STATE, STATE_MACHINE, TRANSITIONS, TIMESTAMP, PREVIOUS_STATE, NEW_STATE, CONFIG_MANDATORY_KEYS

class ElementFiniteStateMachine:

    def __init__(self, config: dict):
        """
        Initialize the FiniteElementStateMachine.

        :param config: dict. The configuration of the FiniteElementStateMachine.
        """
        assert all((key in CONFIG_MANDATORY_KEYS for key in config)), f'Element Finite State Machine have an invalid config. It should contain the following keys: {CONFIG_MANDATORY_KEYS}. Got: {config.keys()}.'
        self.current_state = config[INITIAL_STATE]
        self.transitions = config[TRANSITIONS]
        self.state_machine = config[STATE_MACHINE]
        assert type(self.current_state) == str, f"Element Finite State Machine have an invalid config. 'initial_state' should be a string. Got: {type(self.current_state)}."
        assert type(self.transitions) == dict, f"Element Finite State Machine have an invalid config. 'transitions' should be a dict. Got: {type(self.transitions)}."
        assert all((callable(transition_function) for transition_function in self.transitions.values())), f"Element Finite State Machine have an invalid config. All 'transitions' should be a pair of {{'string' : callable}}. Got: " + f'{self.transitions}.'
        assert type(self.state_machine) == dict, f"Element Finite State Machine have an invalid config. 'state_machine' should be a dict. Got: {type(self.state_machine)}."
        assert all((type(state_transitions) == dict for state_transitions in self.state_machine.values())), f"Element Finite State Machine have an invalid config. All 'state_machine' should be a dict. Got: {self.state_machine}."
        assert all((all((type(transition_id) == str and type(target_state) == str for (transition_id, target_state) in state_transitions.items())) for state_transitions in self.state_machine.values())), f"Element Finite State Machine have an invalid config. All 'state_machine' entries should have the form  'current_state' : {{'transition_id' : 'target_state'}}. Got: " + f'{self.state_machine}.'
        self.history = []

    def __str__(self, default_tabs=2):
        default_tabs = '\t' * default_tabs
        text = '' if len(self.history) > 0 else f'Always in {self.current_state} state.\n'
        for change in self.history:
            (timestamp, prev_state, new_state) = (change[TIMESTAMP], change[PREVIOUS_STATE], change[NEW_STATE])
            text += f'{default_tabs} At: {time_as_str(timestamp, time_format=TIME_FORMAT)} - From : {prev_state} to {new_state}.\n'
        return text

    def update_state(self, prev_element_state, current_element_state):
        """
        Update the current state of the FiniteElementStateMachine.

        :param prev_element_state: ElementState or Child Class. The previous element state.
        :param current_element_state: ElementState. The current element state.
        """
        current_state_transitions = self.state_machine[self.current_state]
        for (transition_id, target_state) in current_state_transitions.items():
            if self.transitions[transition_id](prev_element_state, current_element_state):
                state_change = {TIMESTAMP: current_element_state.timestamp, PREVIOUS_STATE: self.current_state, NEW_STATE: target_state}
                self.current_state = target_state
                self.history.append(state_change)
                break

    def merge(self, other_finite_state_machine: 'ElementFiniteStateMachine'):
        """
        Merge two FiniteElementStateMachines.

        :param other_finite_state_machine: ElementFiniteStateMachine. The other finite state machine.
        """
        assert all((transition_key in other_finite_state_machine.transitions for transition_key in self.transitions)), f'Both finite state machines have different transitions. They are not safe to merge. Got: {self.transitions.keys()} and {other_finite_state_machine.transitions.keys()}.'
        self.history.extend(other_finite_state_machine.history)