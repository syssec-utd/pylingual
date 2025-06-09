def wantClass(self, cls):
    """Is the class a wanted test class?

        A class must be a unittest.TestCase subclass, or match test name
        requirements. Classes that start with _ are always excluded.
        """
    declared = getattr(cls, '__test__', None)
    if declared is not None:
        wanted = declared
    else:
        wanted = not cls.__name__.startswith('_') and (issubclass(cls, unittest.TestCase) or self.matches(cls.__name__))
    plug_wants = self.plugins.wantClass(cls)
    if plug_wants is not None:
        log.debug('Plugin setting selection of %s to %s', cls, plug_wants)
        wanted = plug_wants
    log.debug('wantClass %s? %s', cls, wanted)
    return wanted