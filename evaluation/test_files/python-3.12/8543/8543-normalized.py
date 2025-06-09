def value_to_string(self, obj):
    """Prepare field for serialization."""
    if DJANGO_VERSION > (1, 9):
        value = self.value_from_object(obj)
    else:
        value = self._get_val_from_obj(obj)
    return self.get_prep_value(value)