def set_attributes(self, kwargs):
    """
        Initalizes the given argument structure as properties of the class
        to be used by name in specific method execution.

        Parameters
        ----------
        kwargs : dictionary
            Dictionary of extra attributes,
            where keys are attributes names and values attributes values.

        """
    for (key, value) in kwargs.items():
        setattr(self, key, value)