def belongs_to(self, block):
    """
        Let the given block or network manage the parameters of this layer.
        :param block: Block or NeuralNetwork
        :return: NeuralLayer
        """
    if self._linked_block:
        raise SystemError('The layer {} has already blonged to {}'.format(self.name, self._linked_block.name))
    self._linked_block = block
    block.register_layer(self)
    return self