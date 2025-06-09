def delete(self, instance, disconnect=True):
    """
        Delete an *instance* from the instance pool and optionally *disconnect*
        it from any links it might be connected to. If the *instance* is not
        part of the metaclass, a *MetaException* is thrown.
        """
    if instance in self.storage:
        self.storage.remove(instance)
    else:
        raise DeleteException('Instance not found in the instance pool')
    if not disconnect:
        return
    for link in self.links.values():
        if instance not in link:
            continue
        for other in link[instance]:
            unrelate(instance, other, link.rel_id, link.phrase)