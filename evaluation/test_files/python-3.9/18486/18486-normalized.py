def rvalues(self):
    """ 
        in reversed order
        """
    tmp = self
    while tmp is not None:
        yield tmp.data
        tmp = tmp.prev