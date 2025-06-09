def truthyAttrs(cls):
    """
        Class decorator: override __bool__ to set truthiness based on any attr being present.

        Args:
            cls (class): class to decorate

        Returns:
            class: same, but modified, class
        """

    def __bool__(self):
        return bool(any((getattr(self, attr) for attr in self.attrs)))
    cls.__bool__ = cls.__nonzero__ = __bool__
    return cls