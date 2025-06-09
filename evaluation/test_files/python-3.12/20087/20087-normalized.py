def new(self, *args, **kwargs):
    """
        Create and return a new instance.
        """
    inst = self.clazz()
    self.storage.append(inst)
    referential_attributes = dict()
    for name, ty in self.attributes:
        if name not in self.referential_attributes:
            value = self.default_value(ty)
            setattr(inst, name, value)
    for attr, value in zip(self.attributes, args):
        name, ty = attr
        if name not in self.referential_attributes:
            setattr(inst, name, value)
        else:
            referential_attributes[name] = value
    for name, value in kwargs.items():
        if name not in self.referential_attributes:
            setattr(inst, name, value)
        else:
            referential_attributes[name] = value
    if not referential_attributes:
        return inst
    for link in self.links.values():
        if set(link.key_map.values()) - set(referential_attributes.keys()):
            continue
        kwargs = dict()
        for key, value in link.key_map.items():
            kwargs[key] = referential_attributes[value]
        if not kwargs:
            continue
        for other_inst in link.to_metaclass.query(kwargs):
            relate(other_inst, inst, link.rel_id, link.phrase)
    for name, value in referential_attributes.items():
        if getattr(inst, name) != value:
            logger.warning('unable to assign %s to %s', name, inst)
    return inst