def decode(self, x):
    """
        Decode given representation.
        """
    if not self.rep_dim:
        raise Exception('rep_dim must be set to decode.')
    if not self.decoding_network:
        self.decoding_network = NeuralNetwork(self.rep_dim)
        for layer in self.decoding_layers:
            self.decoding_network.stack_layer(layer, no_setup=True)
    return self.decoding_network.compute(x)