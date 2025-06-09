def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
    """Updates declared fields with fields converted from the SQLAlchemy model
        passed as the `model` class Meta option.
        """
    opts = klass.opts
    Converter = opts.model_converter
    converter = Converter(schema_cls=klass)
    declared_fields = super(SchemaMeta, mcs).get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)
    fields = mcs.get_fields(converter, opts, declared_fields, dict_cls)
    fields.update(declared_fields)
    return fields