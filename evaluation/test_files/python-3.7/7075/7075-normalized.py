def validate(self):
    """
        Verify that the value of the Boolean object is valid.

        Raises:
            TypeError: if the value is not of type bool.
        """
    if self.value:
        if not isinstance(self.value, bool):
            raise TypeError('expected: {0}, observed: {1}'.format(bool, type(self.value)))