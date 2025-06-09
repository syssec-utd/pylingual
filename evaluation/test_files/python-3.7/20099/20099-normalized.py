def define_unique_identifier(self, kind, name, *named_attributes):
    """
        Define a unique identifier for some *kind* of class based on its
        *named attributes*.
        """
    if not named_attributes:
        return
    if isinstance(name, int):
        name = 'I%d' % name
    metaclass = self.find_metaclass(kind)
    metaclass.indices[name] = tuple(named_attributes)
    metaclass.identifying_attributes |= set(named_attributes)