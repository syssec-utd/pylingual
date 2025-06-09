def build_url_field(self, field_name, model_class):
    """
        This is needed due to DRF's model serializer uses the queryset to build url name

        # TODO: Move this to own serializer mixin or fix problem elsewhere?
        """
    field, kwargs = super().build_url_field(field_name, model_class)
    view = self.root.context['view']
    kwargs['view_name'] = view.get_url_name('detail')
    return (field, kwargs)