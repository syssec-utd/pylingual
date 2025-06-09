def add_field(self, model, field):
    """Ran when a field is added to a model."""
    for key in self._iterate_required_keys(field):
        self._create_hstore_required(model._meta.db_table, field, key)