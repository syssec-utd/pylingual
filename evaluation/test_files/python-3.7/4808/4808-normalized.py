def create_model(self, model):
    """Ran when a new model is created."""
    for field in model._meta.local_fields:
        if not isinstance(field, HStoreField):
            continue
        self.add_field(model, field)