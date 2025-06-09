"""Wrapper collection.

Personally speaking, I do NOT like wrappers.
Need deep consideration before staging these wrappers.

First, testing wrappers are hard ...
Suppose we have 5 wrappers, then the total # of possible usage is

325 =
5 +                // 1 wrapper used
5 * 4 +            // 2 wrappers used
5 * 4 * 3 +        // 3
5 * 4 * 3 * 2 +    // 4
5!                 // 5

Testing all possible combinations are very hard. I really don't want to do this.

Second, while there are many possible usage, the actual usage is very limited.
For example, one may use `auto_reset(time_limit(step_fn))` but may not actually use `time_limit(auto_reset(step_fn))`.
Then, why should we provide these functionality as flexible wrapper?

Third, personally, I feel `env = wrapper(env)` style is not easy to follow what actually happens
"""
import jax
import jax.numpy as jnp
from pgx.core import State
TRUE = jnp.bool_(True)
FALSE = jnp.bool_(False)

def auto_reset(step_fn, init_fn):
    """Auto reset wrapper.

    There are several concerns before staging this wrapper:

    1. Final state (observation)
    When auto restting happened, the termianl (or truncated) state/observation is replaced by initial state/observation,
    This is not problematic if it's termination.
    However, when truncation happened, value of truncated state/observation might be used by agent.
    So we have to preserve the final state (observation) somewhere.
    For example, in Gymnasium,

    https://github.com/Farama-Foundation/Gymnasium/blob/main/gymnasium/wrappers/autoreset.py#L59

    However, currently, truncation does *NOT* actually happens because
    all of Pgx environments (games) are finite-horizon and terminates in reasonable # of steps.
    (NOTE: Chess, Shogi, and Go have `max_termination_steps` option following AlphaZero approach)
    So, curren implementation is enough (so far), and I feel implementing `final_state/observation` is useless and not necessary.

    2. Performance:
    Might harm the performance as it always generates new state.
    Memory usage might be doubled. Need to check.
    """

    def wrapped_step_fn(state: State, action):
        state = jax.lax.cond(state.terminated | state.truncated, lambda : state.replace(steps=jnp.int32(0), terminated=FALSE, truncated=FALSE, reward=jnp.zeros_like(state.reward)), lambda : state)
        state = step_fn(state, action)
        state = jax.lax.cond(state.terminated | state.truncated, lambda : init_fn(state._rng_key).replace(terminated=state.terminated, truncated=state.truncated, reward=state.reward), lambda : state)
        return state
    return wrapped_step_fn

def time_limit(step_fn, max_truncation_steps: int=-1):
    """Time limit wrapper.

    So far, all of Pgx environment are finite-horizon and terminates in reasonable # of steps.
    Thus, this wrapper is useless.
    """

    def wrapped_step_fn(state: State, action):
        state = step_fn(state, action)
        state = jax.lax.cond(~state.terminated & (0 <= max_truncation_steps) & (max_truncation_steps <= state._step_count), lambda : state.replace(truncated=TRUE), lambda : state)
        return state
    return wrapped_step_fn