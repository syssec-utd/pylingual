def populate_associations(self, metamodel):
    """
        Populate a *metamodel* with associations previously encountered from
        input.
        """
    for stmt in self.statements:
        if not isinstance(stmt, CreateAssociationStmt):
            continue
        ass = metamodel.define_association(stmt.rel_id, stmt.source_kind, stmt.source_keys, 'M' in stmt.source_cardinality, 'C' in stmt.source_cardinality, stmt.source_phrase, stmt.target_kind, stmt.target_keys, 'M' in stmt.target_cardinality, 'C' in stmt.target_cardinality, stmt.target_phrase)
        ass.formalize()