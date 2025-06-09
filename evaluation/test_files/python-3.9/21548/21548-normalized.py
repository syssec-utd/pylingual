def proxied_attribute(local_attr, proxied_attr, doc):
    """Create a property that proxies attribute ``proxied_attr`` through
    the local attribute ``local_attr``.
    """

    def fget(self):
        return getattr(getattr(self, local_attr), proxied_attr)

    def fset(self, value):
        setattr(getattr(self, local_attr), proxied_attr, value)

    def fdel(self):
        delattr(getattr(self, local_attr), proxied_attr)
    return property(fget, fset, fdel, doc)