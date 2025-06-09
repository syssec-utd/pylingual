def leapfrog_step(leapfrog_step_state: LeapFrogStepState, step_size: FloatTensor, target_log_prob_fn: PotentialFn, kinetic_energy_fn: PotentialFn) -> Tuple[LeapFrogStepState, LeapFrogStepExtras]:
    """Leapfrog `TransitionOperator`.

  Args:
    leapfrog_step_state: LeapFrogStepState.
    step_size: Step size, structure broadcastable to the `target_log_prob_fn`
      state.
    target_log_prob_fn: Target log prob fn.
    kinetic_energy_fn: Kinetic energy fn.

  Returns:
    leapfrog_step_state: LeapFrogStepState.
    leapfrog_step_extras: LeapFrogStepExtras.
  """
    state = leapfrog_step_state.state
    state_grads = leapfrog_step_state.state_grads
    momentum = leapfrog_step_state.momentum
    step_size = maybe_broadcast_structure(step_size, state)
    state = tf.nest.map_structure(tf.convert_to_tensor, state)
    momentum = tf.nest.map_structure(tf.convert_to_tensor, momentum)
    state = tf.nest.map_structure(tf.convert_to_tensor, state)
    if state_grads is None:
        (_, _, state_grads) = call_and_grads(target_log_prob_fn, state)
    else:
        state_grads = tf.nest.map_structure(tf.convert_to_tensor, state_grads)
    momentum = tf.nest.map_structure(lambda m, sg, s: m + 0.5 * sg * s, momentum, state_grads, step_size)
    (kinetic_energy, kinetic_energy_extra, momentum_grads) = call_and_grads(kinetic_energy_fn, momentum)
    state = tf.nest.map_structure(lambda x, mg, s: x + mg * s, state, momentum_grads, step_size)
    (target_log_prob, state_extra, state_grads) = call_and_grads(target_log_prob_fn, state)
    momentum = tf.nest.map_structure(lambda m, sg, s: m + 0.5 * sg * s, momentum, state_grads, step_size)
    return (LeapFrogStepState(state, state_grads, momentum), LeapFrogStepExtras(target_log_prob, state_extra, kinetic_energy, kinetic_energy_extra))