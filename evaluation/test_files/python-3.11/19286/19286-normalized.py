def defaults_(self):
    """Iterator over sections, option names, and option metadata.

        This iterator is also implemented at the section level. The two loops
        produce the same output::

            for sct, opt, meta in conf.defaults_():
                print(sct, opt, meta.default)

            for sct in conf.sections_():
                for opt, meta in conf[sct].defaults_():
                    print(sct, opt, meta.default)

        Yields:
            tuples with sections, option names, and :class:`Conf` instances
            holding option metadata.
        """
    for sct, opt in self.options_():
        yield (sct, opt, self[sct].def_[opt])