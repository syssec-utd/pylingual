from django.apps import AppConfig as DjangoAppConfig

class AppConfig(DjangoAppConfig):
    name = 'meta_ae'
    verbose_name = 'META Adverse Events'
    include_in_administration_section = True
    has_exportable_data = True
    default_auto_field = 'django.db.models.BigAutoField'