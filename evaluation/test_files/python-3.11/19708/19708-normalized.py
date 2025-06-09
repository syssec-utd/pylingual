def readonly(cls, *args, **kwargs):
    """
        Return an already closed read-only instance of Fridge.
        Arguments are the same as for the constructor.
        """
    fridge = cls(*args, **kwargs)
    fridge.close()
    return fridge