"""
The module :mod:`piaf.behavior` contains everything related to behaviors.

Behaviors are small execution units that run "concurrently": several behaviors can be
active at the same time but only one is executed per agent.

Behaviors have access to the agent they are bounded to and are the preferred way to
manipulate it, like updating its knowledge, sending or receiving messages.
"""
from __future__ import annotations
import abc
import asyncio
import logging
from typing import Any, Callable, Dict, Type, Optional
import piaf.agent
__all__ = ['Behavior', 'CyclicBehavior', 'FSMBehavior']

class Behavior(metaclass=abc.ABCMeta):
    """
    Base class user behaviors.

    When creating a behavior, you have to subclass :class:`Behavior` and provide at
    least  an implementation for the :meth:`action` method.

    You can also override the :meth:`done` method. This method is called when
    :meth:`action` method ends and according to the returned value, decide if
    the behavior ends or if the :meth:`action` method should be executed again.

    You should know that between two calls to :meth:`action`, a another
    behavior can be executed. It is also true when you are using the keyword
    ``await`` (mostlikely when you send or receive a message).

    You can access to the agent with the ``agent`` attribute.
    """

    def __init__(self, agent: piaf.agent.Agent):
        """
        Take an :class:`Agent` and construct a behavior with it.

        :param agent: the agent that will execute the behavior
        """
        self.agent = agent
        self.logger = logging.getLogger(type(self).__name__)

    async def run(self) -> None:
        """
        Run the behavior.

        This coroutine won't end until the :meth:`done` method returns
        ``False``. It also take care of the agent state: between two calls to
        method :meth:`action`, the agent's state is checked. The behavior will
        be paused if the agent's state is not ``AgentState.ACTIVE``.

        .. warning:: You should not override this method. To provide a custom body
                     to your behavior, implements the :meth:`action` method instead.
        """
        done = False
        while not done:
            async with self.agent.state_sync:
                await self.agent.state_sync.wait_for(lambda : self.agent.state == piaf.agent.AgentState.ACTIVE)
            await self.action()
            done = self.done()
            if not done:
                await asyncio.sleep(0)

    @abc.abstractmethod
    async def action(self) -> None:
        """
        Body of any behavior.

        This method must be implemented. The :meth:`action` method is generally executed
        in a row, except if coroutines are awaited (mostlikely agent's
        :meth:`Agent.send`, :meth:`Agent.receive` or :meth:`Agent.receive_nowait`
        methods). Because of this, the :meth:`action` method shouldn't make expensive
        blocking operations, as it will slow down the entire platform.

        If you want to run expensive IO or CPU operations, use
        :func:`asyncio.run_in_executor` and await the result.
        """
        raise NotImplementedError()

    def done(self) -> bool:
        """
        Indicate wether or not this behavior is done.

        When this function `returns ``True``, the behavior's :meth:`run` method ends.
        Default implementation always return True.
        """
        return True

    def result(self) -> Any:
        """
        Get this behavior's result.

        Sometimes you might want to transmit a value. Rather than using an agent's
        attribute, you can use this method to fetch the result. Default is to return
        ``None``.
        """
        return None

class CyclicBehavior(Behavior, metaclass=abc.ABCMeta):
    """
    :class:`CyclicBehavior` are behaviors with a cyclic execution.

    Each time the :meth:`action` method execution finishes, a delay is applied before
    the next call. You can access (and modify) this delay using the ``delay`` attribute.

    Except this, it is a normal behavior.
    """

    def __init__(self, agent: piaf.agent.Agent, delay: float):
        """
        Create a :class:`CyclicBehavior`.

        The delay will pause the behavior between successive calls to method
        :meth:`action`.
        """
        super().__init__(agent)
        self.delay = delay

    def done(self) -> bool:
        """
        Indicate wether or not this behavior is done.

        When this function `returns ``True``, the behavior's :meth:`run` method ends.
        Default implementation always return False.
        """
        return False

    async def run(self) -> None:
        """
        Run the behavior.

        This coroutine won't end until the :meth:`done` method returns
        ``False``. It also take care of the agent state: between two calls to
        method :meth:`action`, the agent's state is checked. The behavior will
        be paused if the agent's state is ``AgentState.SUSPENDED``.

        The delay is applied between successive calls to :meth:`action`.

        .. warning:: You should not override this method. To provide a custom body
                     to your behavior, implements the :meth:`action` method instead.
        """
        done = False
        while not done:
            async with self.agent.state_sync:
                await self.agent.state_sync.wait_for(lambda : self.agent.state == piaf.agent.AgentState.ACTIVE)
            await self.action()
            done = self.done()
            await asyncio.sleep(self.delay)

class _FSMState:
    """
    Used internally by the :class:`FSMBehavior` to represent states.

    This class is more like a data class that store information about states:

    ``name``: the state's name
    ``behavior``: the behavior class associated to the state
    ``transition``: a mapping function -> state
    ``final``: whether this state is a final state or not
    ``args``: a sequence of things that will be used to instantiate the behavior
    ``kwargs``: same as ``args`` but for keyword arguments

    """

    def __init__(self, name: str, behavior: Type[Behavior], args, kwargs, final: bool=False):
        super().__init__()
        self.name = name
        self.behavior = behavior
        self.transitions: Dict[Callable[[Any], bool], _FSMState] = {}
        self.final = final
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, value):
        return type(value) == type(self) and value.name == self.name

    def __hash__(self):
        return hash(self.name)

class FSMBehavior(Behavior):
    """
    Complex behavior that mimic a Final State Machine.

    To each state is associated a behavior that will be executed when the FSM enters in
    the associated state. Behaviors are instanciated each time.

    Like any FSM, you will need to identify which states are final and which is the
    initial state.

    Transitions made with functions with the following signature:
    ``Callable[[Any], bool]``. If the returned value is ``True``, then the FSM can
    transition to the targeted state. The function's argument will be fullfilled with
    the previous executed behavior result.

    Here is an example::

        # Create the behavior
        bhv = piaf.behavior.FSMBehavior(agent)

        # Four states: A, B, C and D
        # D is a final state
        bhv.add_state("A", ABehavior)
        bhv.add_state("B", BBehavior, args=(foo, ))
        bhv.add_state("C", CBehavior)
        bhv.add_state("D", DBehavior, args=(foo, bar), final=True)

        # Now A is our initial state
        bhv.set_initial_state("A")

        # Declare transitions.
        # Here our behaviors are returning a letter as result. We use it to make our
        # transition function.
        bhv.add_transition("A", "B", lambda r: r == "B")
        bhv.add_transition("A", "C", lambda r: r == "C")
        bhv.add_transition("B", "A", lambda r: r == "A")
        bhv.add_transition("C", "A", lambda r: r == "A")
        bhv.add_transition("C", "B", lambda r: r == "B")
        bhv.add_transition("B", "D", lambda r: r == "D")

    """

    def __init__(self, agent: piaf.agent.Agent):
        """Create a new :class:`FSMBehavior`. No states at the beginning."""
        super().__init__(agent)
        self._states: Dict[str, _FSMState] = {}
        self._initial: Optional[str] = None
        self._c_state: Optional[str] = None
        self._c_task: Optional[asyncio.Future[None]] = None
        self._last_result: Any = None

    def set_initial_state(self, name: str):
        """
        Set the provided state as the initial state.

        It will replace the previous selected one. Do not call this method once the
        behavior has been added to an agent.

        :param name: the state that will be the initial state
        """
        if name not in self._states:
            raise Exception()
        self._initial = name

    def add_state(self, name: str, behavior: Type[Behavior], args=None, kwargs=None, final: bool=False):
        """
        Create a new state and associate the provided behavior.

        Names must be uniques for a given FSM. You must supply a behavior class (not
        an instance). When the state will be reached at execution time, the behavior
        will be instantiated and the FSM will wait until its completion to transition
        to the newt state.

        :param name: the state's name
        :param behavior: the behavior's class associated to this state
        :pram args: Optional. Should be a sequence of parameters required to your
                    behavior's instantiation (except for the ``agent`` parameter
                    that is automatically supplied)
        :param kwargs: same as ``args`` but for keywords arguments
        :param final: Is this state a final state ? Default is ``False``
        """
        if name in self._states:
            raise Exception()
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        self._states[name] = _FSMState(name, behavior, args, kwargs, final)

    def add_transition(self, from_: str, to_: str, func: Callable[[Any], bool]):
        """
        Add a transition between two states.

        The provided function will be used to decide if the transition is possible or
        not given the previous behavior result. Given a state, it shouldn't be possible
        to have two possible transition (meaning, two functions that returns true for
        two different states). This bad design can't be recognized, so extra
        carefullness is required here.

        :param from_: first state
        :param to_: second state
        :param func: transition function
        :raise ValueError: if either ``from_`` or ``to_`` state doesn't exist
        """
        try:
            from_s = self._states[from_]
        except KeyError:
            raise ValueError(f'Unknown state: {from_}')
        try:
            from_s.transitions[func] = self._states[to_]
        except KeyError:
            raise ValueError(f'Unknown state: {to_}')

    async def run(self) -> None:
        """
        Run the behavior.

        This coroutine won't end until the :meth:`done` method returns
        ``False``. It also take care of the agent state: between two calls to
        method :meth:`action`, the agent's state is checked. The behavior will
        be paused if the agent's state is ``AgentState.SUSPENDED``.

        A check will be performed just before running the behavior to ensure that:

        * There is an initial state
        * At least one final state is accessible
        * Not final states have at least one exit transition to another state
        * All  states are reachable

        The later will produce a warning each time a state can't be reached. The
        other three will raise an exception and prevent the behavior to be run.
        """
        self._check_fsm()
        await super().run()

    async def action(self) -> None:
        """
        :class:`FSMBehavior`'s body.

        Unlike :class:`Behavior`, there is no need to override this method. It will
        raise an exception if during execution there is no transition available and
        the current node is not final (FSM is stuck).
        """
        assert self._initial is not None
        if self._c_state is None:
            self._c_state = self._initial
        else:
            found = False
            for (func, state) in self._states[self._c_state].transitions.items():
                if func(self._last_result):
                    self._c_state = state.name
                    found = True
                    break
            if not found:
                raise Exception()
        state = self._states[self._c_state]
        bhv = state.behavior(self.agent, *state.args, **state.kwargs)
        self._c_task = self.agent.add_behavior(bhv)
        await self._c_task
        self._last_result = bhv.result()

    def done(self) -> bool:
        """
        Indicate wether or not this behavior is done.

        When a final state is reached, this behavior will end (after the state's
        associated behavior execution).
        """
        assert self._c_state is not None
        assert self._c_task is not None
        return self._states[self._c_state].final

    def _check_fsm(self):
        if self._states.get(self._initial, None) is None:
            raise Exception()
        visited = set()
        new_visited = {self._states[self._initial]}
        finals = set()
        if self._states[self._initial].final:
            finals.add(self._states[self._initial])
        while len(visited) != len(new_visited):
            visited = set(new_visited)
            for state in visited:
                for child in state.transitions.values():
                    new_visited.add(child)
                    if child.final:
                        finals.add(child)
                    elif not child.transitions:
                        raise Exception()
        unreachable = set(self._states.values()).difference(visited)
        for state in unreachable:
            self.logger.warning('[%s] Unreachable state: %s', self.agent.aid.short_name, state.name)
        if finals.issubset(unreachable):
            raise Exception()

class SuicideBehavior(Behavior):
    """
    One-shot behavior killing the owner.

    A typicall usage is to associate this behavior to the final state of a :class:`FSMBehavior` instance. Although it
    only calls :meth:`Agent.quit()`, this behavior avoids duplication accross dependent projects.
    """

    async def action(self) -> None:
        """Make the owner quit as soon as possible."""
        await self.agent.quit()