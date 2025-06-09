def navigate(self, inst, kind, rel_id, phrase=''):
    """
        Navigate across a link with some *rel_id* and *phrase* that yields
        instances of some *kind*.
        """
    key = (kind.upper(), rel_id, phrase)
    if key in self.links:
        link = self.links[key]
        return link.navigate(inst)
    link1, link2 = self._find_assoc_links(kind, rel_id, phrase)
    inst_set = xtuml.OrderedSet()
    for inst in link1.navigate(inst):
        inst_set |= link2.navigate(inst)
    return inst_set