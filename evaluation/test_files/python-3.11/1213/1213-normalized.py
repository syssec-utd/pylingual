def _maybe_broadcast_volatility(volatility_parts, state_parts):
    """Helper to broadcast `volatility_parts` to the shape of `state_parts`."""
    return [v + tf.zeros_like(sp, dtype=sp.dtype.base_dtype) for v, sp in zip(volatility_parts, state_parts)]