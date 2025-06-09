def get_relationship(self, from_object, relation_type):
    """return a relation ship or None
        """
    for rel in self.relationships.get(relation_type, ()):
        if rel.from_object is from_object:
            return rel
    raise KeyError(relation_type)