def init(self, ctxt, step_addr):
    """
        Initialize the item.  This calls the class constructor with the
        appropriate arguments and returns the initialized object.

        :param ctxt: The context object.
        :param step_addr: The address of the step in the test
                          configuration.
        """
    return self.cls(ctxt, self.name, self.conf, step_addr)