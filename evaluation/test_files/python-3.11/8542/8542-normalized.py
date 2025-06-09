def formfield(self, **kwargs):
    """Return a formfield."""
    defaults = {}
    if self.ppoi_field:
        defaults['form_class'] = SizedImageCenterpointClickDjangoAdminField
    if kwargs.get('widget') is AdminFileWidget:
        del kwargs['widget']
    defaults.update(kwargs)
    return super(VersatileImageField, self).formfield(**defaults)