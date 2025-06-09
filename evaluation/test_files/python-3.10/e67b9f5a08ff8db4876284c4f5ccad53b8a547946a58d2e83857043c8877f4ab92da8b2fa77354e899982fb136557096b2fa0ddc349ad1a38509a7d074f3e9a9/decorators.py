from typing import Any
from django.db.models.base import ModelBase

def field_default(field: str, default: Any):

    def decorator(cls: ModelBase):
        model_field = cls._meta.get_field(field)
        model_field.default = default
        return cls
    return decorator