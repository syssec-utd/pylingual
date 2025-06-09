def stack_reparameterization_layer(self, layer_size):
    """
        Perform reparameterization trick for latent variables.
        :param layer_size: the size of latent variable
        """
    self.rep_layer = ReparameterizationLayer(layer_size, sample=self.sample)
    self.stack_encoders(self.rep_layer)