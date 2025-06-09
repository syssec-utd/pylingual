"""
``web_poet.fields`` is a module with helpers for putting extraction logic
into separate Page Object methods / properties.
"""
import inspect
from contextlib import suppress
from functools import update_wrapper, wraps
from typing import Callable, Dict, List, Optional, Type, TypeVar
import attrs
from itemadapter import ItemAdapter
from web_poet.utils import cached_method, ensure_awaitable
_FIELDS_INFO_ATTRIBUTE_READ = '_web_poet_fields_info'
_FIELDS_INFO_ATTRIBUTE_WRITE = '_web_poet_fields_info_temp'

@attrs.define
class FieldInfo:
    """Information about a field"""
    name: str
    meta: Optional[dict] = None
    out: Optional[List[Callable]] = None

class FieldsMixin:
    """A mixin which is required for a class to support fields"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        this_class_fields = getattr(cls, _FIELDS_INFO_ATTRIBUTE_WRITE, {})
        base_class_fields = getattr(cls, _FIELDS_INFO_ATTRIBUTE_READ, {})
        if base_class_fields or this_class_fields:
            fields = {**base_class_fields, **this_class_fields}
            setattr(cls, _FIELDS_INFO_ATTRIBUTE_READ, fields)
            with suppress(AttributeError):
                delattr(cls, _FIELDS_INFO_ATTRIBUTE_WRITE)

def field(method=None, *, cached: bool=False, meta: Optional[dict]=None, out: Optional[List[Callable]]=None):
    """
    Page Object method decorated with ``@field`` decorator becomes a property,
    which is then used by :class:`~.ItemPage`'s to_item() method to populate
    a corresponding item attribute.

    By default, the value is computed on each property access.
    Use ``@field(cached=True)`` to cache the property value.

    The ``meta`` parameter allows to store arbitrary information for the field,
    e.g. ``@field(meta={"expensive": True})``. This information can be later
    retrieved for all fields using the :func:`get_fields_dict` function.

    The ``out`` parameter is an optional list of field processors, which are
    functions applied to the value of the field before returning it.
    """

    class _field:

        def __init__(self, method):
            if not callable(method):
                raise TypeError(f'@field decorator must be used on methods, {method!r} is decorated instead')
            method = self._processed(method)
            if cached:
                self.unbound_method = cached_method(method)
            else:
                self.unbound_method = method

        def __set_name__(self, owner, name):
            if not hasattr(owner, _FIELDS_INFO_ATTRIBUTE_WRITE):
                setattr(owner, _FIELDS_INFO_ATTRIBUTE_WRITE, {})
            field_info = FieldInfo(name=name, meta=meta, out=out)
            getattr(owner, _FIELDS_INFO_ATTRIBUTE_WRITE)[name] = field_info

        def __get__(self, instance, owner=None):
            return self.unbound_method(instance)

        @staticmethod
        def _process(value):
            for processor in out:
                value = processor(value)
            return value

        def _processed(self, method):
            """Returns a wrapper for method that calls processors on its result"""
            if not out:
                return method
            if inspect.iscoroutinefunction(method):

                async def processed(*args, **kwargs):
                    return self._process(await method(*args, **kwargs))
            else:

                def processed(*args, **kwargs):
                    return self._process(method(*args, **kwargs))
            return wraps(method)(processed)
    if method is not None:
        res = _field(method)
        update_wrapper(res, method)
        return res
    else:
        return _field

def get_fields_dict(cls_or_instance) -> Dict[str, FieldInfo]:
    """Return a dictionary with information about the fields defined
    for the class: keys are field names, and values are
    :class:`web_poet.fields.FieldInfo` instances.
    """
    return getattr(cls_or_instance, _FIELDS_INFO_ATTRIBUTE_READ, {})
T = TypeVar('T')

async def item_from_fields(obj, item_cls: Type[T]=dict, *, skip_nonitem_fields: bool=False) -> T:
    """Return an item of ``item_cls`` type, with its attributes populated
    from the ``obj`` methods decorated with :class:`field` decorator.

    If ``skip_nonitem_fields`` is True, ``@fields`` whose names are not
    among ``item_cls`` field names are not passed to ``item_cls.__init__``.

    When ``skip_nonitem_fields`` is False (default), all ``@fields`` are passed
    to ``item_cls.__init__``, possibly causing exceptions if
    ``item_cls.__init__`` doesn't support them.
    """
    item_dict = item_from_fields_sync(obj, item_cls=dict, skip_nonitem_fields=False)
    field_names = list(item_dict.keys())
    if skip_nonitem_fields:
        field_names = _without_unsupported_field_names(item_cls, field_names)
    return item_cls(**{name: await ensure_awaitable(item_dict[name]) for name in field_names})

def item_from_fields_sync(obj, item_cls: Type[T]=dict, *, skip_nonitem_fields: bool=False) -> T:
    """Synchronous version of :func:`item_from_fields`."""
    field_names = list(get_fields_dict(obj))
    if skip_nonitem_fields:
        field_names = _without_unsupported_field_names(item_cls, field_names)
    return item_cls(**{name: getattr(obj, name) for name in field_names})

def _without_unsupported_field_names(item_cls: type, field_names: List[str]) -> List[str]:
    item_field_names = ItemAdapter.get_field_names_from_class(item_cls)
    if item_field_names is None:
        return field_names[:]
    return list(set(field_names) & set(item_field_names))