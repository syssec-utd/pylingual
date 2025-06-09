def populate_instances(self, metamodel):
    """
        Populate a *metamodel* with instances previously encountered from
        input.
        """
    for stmt in self.statements:
        if not isinstance(stmt, CreateInstanceStmt):
            continue
        if stmt.names:
            fn = self._populate_instance_with_named_arguments
        else:
            fn = self._populate_instance_with_positional_arguments
        fn(metamodel, stmt)