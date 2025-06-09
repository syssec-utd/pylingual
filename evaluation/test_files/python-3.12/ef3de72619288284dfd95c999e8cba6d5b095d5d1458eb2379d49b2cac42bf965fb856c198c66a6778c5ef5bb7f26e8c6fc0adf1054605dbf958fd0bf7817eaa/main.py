import functools
import inspect
from typing import Any, Dict, Optional, cast, no_type_check
from extendable import context
from extendable.main import ExtendableMeta
from extendable.registry import ExtendableClassesRegistry, ExtendableRegistryListener
from pydantic.fields import ModelField
from pydantic.generics import GenericModel
from pydantic.main import BaseModel, ModelMetaclass

class ExtendableModelMeta(ExtendableMeta, ModelMetaclass):

    @no_type_check
    @classmethod
    def _build_original_class(metacls, name, bases, namespace, **kwargs):
        return ModelMetaclass.__new__(metacls, name, bases, namespace, **kwargs)

    @no_type_check
    @classmethod
    def _prepare_namespace(metacls, name, bases, namespace, extends=None, **kwargs) -> Dict[str, Any]:
        namespace = super()._prepare_namespace(name=name, bases=bases, namespace=namespace, extends=extends, **kwargs)
        if BaseModel in bases or GenericModel in bases:
            metacls._wrap_pydantic_base_model_class_methods(namespace)
        return namespace

    @classmethod
    def _wrap_pydantic_base_model_class_methods(metacls, namespace: Dict[str, Any]) -> Dict[str, Any]:
        new_namespace = namespace
        methods = inspect.getmembers(BaseModel, inspect.ismethod)
        for name, method in methods:
            func = method.__func__
            if name.startswith('__'):
                continue
            if name in namespace:
                continue

            @no_type_check
            def new_method(cls, *args, _method_name=None, _initial_func=None, **kwargs):
                inspect.signature(_initial_func).bind(cls, *args, **kwargs)
                if getattr(cls, '_is_aggregated_class', False) or hasattr(cls, '_original_cls'):
                    return _initial_func(cls, *args, **kwargs)
                cls = cls._get_assembled_cls()
                return getattr(cls, _method_name)(*args, **kwargs)
            new_method_def = functools.partial(new_method, _method_name=name, _initial_func=func)
            functools.update_wrapper(new_method_def, func)
            new_namespace[name] = classmethod(new_method_def)
        return new_namespace

    def _resolve_submodel_fields(cls, registry: Optional[ExtendableClassesRegistry]=None) -> None:
        """Replace the original field type into the definition of the field by the one
        from the registry."""
        registry = registry if registry else context.extendable_registry.get()
        if issubclass(cls, BaseModel):
            for field in cast(BaseModel, cls).__fields__.values():
                cast(ExtendableModelMeta, cls)._resolve_submodel_field(field, registry)

    def _resolve_submodel_field(cls, field: ModelField, registry: ExtendableClassesRegistry) -> None:
        if issubclass(type(field.type_), ExtendableModelMeta):
            field.type_ = field.type_._get_assembled_cls(registry)
            field.prepare()
        if field.sub_fields:
            for sub_f in field.sub_fields:
                cls._resolve_submodel_field(sub_f, registry)

class RegistryListener(ExtendableRegistryListener):

    def on_registry_initialized(self, registry: ExtendableClassesRegistry) -> None:
        self.update_forward_refs(registry)
        self.resolve_submodel_fields(registry)

    def update_forward_refs(self, registry: ExtendableClassesRegistry) -> None:
        """Try to update ForwardRefs on fields to resolve dynamic type usage."""
        for cls in registry._extendable_classes.values():
            if issubclass(cls, BaseModel):
                cast(BaseModel, cls).update_forward_refs()

    def resolve_submodel_fields(self, registry: ExtendableClassesRegistry) -> None:
        for cls in registry._extendable_classes.values():
            if issubclass(type(cls), ExtendableModelMeta):
                cast(ExtendableModelMeta, cls)._resolve_submodel_fields(registry)
ExtendableClassesRegistry.listeners.append(RegistryListener())