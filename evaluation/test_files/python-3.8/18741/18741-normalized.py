def setModel(self, model):
    """
        Sets the model this actor should use when drawing.
        
        This method also automatically initializes the new model and removes the old, if any.
        """
    if self.model is not None:
        self.model.cleanup(self)
    self.model = model
    model.create(self)