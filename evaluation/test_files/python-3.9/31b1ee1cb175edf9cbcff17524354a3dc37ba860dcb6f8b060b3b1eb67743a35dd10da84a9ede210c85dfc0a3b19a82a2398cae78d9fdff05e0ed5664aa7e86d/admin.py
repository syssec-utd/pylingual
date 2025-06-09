from django import forms
from django.contrib import admin
from eoxserver.backends.storages import get_handlers
from eoxserver.backends import models

def get_storage_type_choices():
    return [(handler.name, handler.name) for handler in get_handlers()]

class StorageForm(forms.ModelForm):
    """ Form for `Storages`. Overrides the `format` formfield and adds choices
        dynamically.
    """

    def __init__(self, *args, **kwargs):
        super(StorageForm, self).__init__(*args, **kwargs)
        self.fields['storage_type'] = forms.ChoiceField(choices=[('---------', None)] + get_storage_type_choices())

class StorageAdmin(admin.ModelAdmin):
    form = StorageForm
    model = models.Storage

    def save_model(self, request, obj, form, change):
        if not obj.name:
            obj.name = None
        super(StorageAdmin, self).save_model(request, obj, form, change)
admin.site.register(models.Storage, StorageAdmin)
admin.site.register(models.StorageAuth)