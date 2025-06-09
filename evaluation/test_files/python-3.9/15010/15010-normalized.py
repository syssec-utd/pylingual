def model_fields_form_factory(model):
    """ Creates a form for specifying fields from a model to display. """
    fields = model._meta.get_fields()
    choices = []
    for field in fields:
        if hasattr(field, 'verbose_name'):
            choices.append((field.name, field.verbose_name))

    class ModelFieldsForm(forms.Form):
        fields = forms.MultipleChoiceField(choices=choices, required=False)
    return ModelFieldsForm