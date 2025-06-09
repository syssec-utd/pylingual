def dagster_type(name=None, description=None, input_schema=None, output_schema=None, serialization_strategy=None, storage_plugins=None):
    """
    Decorator version of as_dagster_type. See documentation for :py:func:`as_dagster_type` .
    """

    def _with_args(bare_cls):
        check.type_param(bare_cls, 'bare_cls')
        new_name = name if name else bare_cls.__name__
        return _decorate_as_dagster_type(bare_cls=bare_cls, key=new_name, name=new_name, description=description, input_schema=input_schema, output_schema=output_schema, serialization_strategy=serialization_strategy, storage_plugins=storage_plugins)
    if callable(name):
        klass = name
        new_name = klass.__name__
        return _decorate_as_dagster_type(bare_cls=klass, key=new_name, name=new_name, description=None)
    return _with_args