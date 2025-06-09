def get_object_id(model, meteor_id):
    """Return an object ID for the given meteor_id."""
    if meteor_id is None:
        return None
    meta = model._meta
    if model is ObjectMapping:
        raise TypeError("Can't map ObjectMapping instances through self.")
    if isinstance(meta.pk, AleaIdField):
        return meteor_id
    alea_unique_fields = [field for field in meta.local_fields if isinstance(field, AleaIdField) and field.unique]
    if len(alea_unique_fields) == 1:
        val = model.objects.values_list('pk', flat=True).get(**{alea_unique_fields[0].attname: meteor_id})
        if val:
            return val
    content_type = ContentType.objects.get_for_model(model)
    return ObjectMapping.objects.filter(content_type=content_type, meteor_id=meteor_id).values_list('object_id', flat=True).get()