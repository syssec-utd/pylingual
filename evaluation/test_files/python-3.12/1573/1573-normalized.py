def mask(self, symbol, on_value, off_value):
    """Produces a masking tensor for (in)valid production rules.

    Args:
      symbol: str, a symbol in the grammar.
      on_value: Value to use for a valid production rule.
      off_value: Value to use for an invalid production rule.

    Returns:
      Tensor of shape [1, num_production_rules]. An element is `on_value`
      if its corresponding production rule has `symbol` on its left-hand-side;
      the element is `off_value` otherwise.
    """
    mask_values = [on_value if lhs == symbol else off_value for lhs, _ in self.production_rules]
    mask_values = tf.reshape(mask_values, [1, len(self.production_rules)])
    return mask_values