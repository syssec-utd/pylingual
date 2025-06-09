from typing import Any, List, cast
from django.contrib.contenttypes.fields import GenericRelation
from django.core import checks
from django.db import DEFAULT_DB_ALIAS
from django.db.models import Field
from django.utils.functional import cached_property
from ... import forms
from ...helpers import _get_item_types
from .base import FileResourceFieldBase

class ContentItemRelation(GenericRelation):
    """
    FIX: cascade delete polymorphic
    https://github.com/django-polymorphic/django-polymorphic/issues/34
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bulk_related_objects(self, objs, using=DEFAULT_DB_ALIAS):
        return super().bulk_related_objects(objs).non_polymorphic()

class CollectionField(FileResourceFieldBase):

    def __init__(self, to, **kwargs):
        kwargs['blank'] = True
        super().__init__(to=to, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if 'blank' in kwargs:
            del kwargs['blank']
        return (name, path, args, kwargs)

    def _check_relation_class(self, base, error_message):
        from ...models.collection import CollectionBase
        rel_is_string = isinstance(self.remote_field.model, str)
        if rel_is_string:
            return []
        model_name = self.remote_field.model if rel_is_string else self.remote_field.model._meta.object_name
        if not issubclass(self.remote_field.model, CollectionBase):
            return [checks.Error("Field defines a relation with model '%s', which is not subclass of CollectionBase" % model_name, obj=self)]
        return []

    def formfield(self, **kwargs):
        return super().formfield(**{'form_class': forms.CollectionField, **kwargs})

class CollectionItem:
    """
    Поле для подключения классов элементов коллекции.
    Может использоваться только в подклассах CollectionBase.
    """
    default_validators = []

    def __init__(self, to, name=None, validators=(), options=None):
        self.name = name
        try:
            to._meta.model_name
        except AttributeError:
            assert isinstance(to, str), '%s(%r) is invalid. First parameter to %s must be a model' % (self.__class__.__name__, to, self.__class__.__name__)
        self.model = to
        self.options = options or {}
        self._validators = list(validators)

    def check(self, **kwargs):
        return [*Field._check_field_name(cast(Field, self)), *Field._check_validators(cast(Field, self))]

    @cached_property
    def validators(self):
        return [*self.default_validators, *self._validators]

    def contribute_to_class(self, cls, name, **kwargs):
        self.name = self.name or name
        item_types = _get_item_types(cls)
        if item_types is not None:
            item_types[self.name] = self