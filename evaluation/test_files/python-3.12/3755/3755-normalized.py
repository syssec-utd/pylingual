def _validate_after_init(init_method):
    """Add validation after instantiation."""

    @wraps(init_method)
    def _decorated(self, **kwargs):
        try:
            _ = self.shallow_schema.validate(kwargs)
        except ValidationError as ex:
            raise ModelValidationError(ex.messages, ex.field_names, ex.fields, ex.data, **ex.kwargs) from None
        init_method(self, **kwargs)
    return _decorated