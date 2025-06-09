def set_default_value(self, obj):
    """Set the default value on a per instance basis.

        This method is called by :meth:`instance_init` to create and
        validate the default value.  The creation and validation of
        default values must be delayed until the parent :class:`HasTraits`
        class has been instantiated.
        """
    mro = type(obj).mro()
    meth_name = '_%s_default' % self.name
    for cls in mro[:mro.index(self.this_class) + 1]:
        if meth_name in cls.__dict__:
            break
    else:
        dv = self.get_default_value()
        newdv = self._validate(obj, dv)
        obj._trait_values[self.name] = newdv
        return
    obj._trait_dyn_inits[self.name] = cls.__dict__[meth_name]