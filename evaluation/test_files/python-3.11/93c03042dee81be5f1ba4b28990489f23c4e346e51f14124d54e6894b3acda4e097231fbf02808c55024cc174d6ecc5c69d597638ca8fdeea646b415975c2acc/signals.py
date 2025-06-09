from django.db.models.signals import post_delete
from django.dispatch import Signal, receiver
from django_tenants.utils import get_tenant_model, schema_exists
post_schema_sync = Signal()
post_schema_sync.__doc__ = '\n\nSent after a tenant has been saved, its schema created and synced\n\nArgument Required = tenant\n\n'
schema_needs_to_be_sync = Signal()
schema_needs_to_be_sync.__doc__ = '\nSchema needs to be synced\n\nArgument Required = tenant\n\n'
schema_migrated = Signal()
schema_migrated.__doc__ = '\nSent after migration has finished on a schema\n\nArgument Required = schema_name\n'
schema_migrate_message = Signal()
schema_migrate_message.__doc__ = '\nSent when a message is generated in run migration\n\nArgument Required = message\n'

@receiver(post_delete)
def tenant_delete_callback(sender, instance, **kwargs):
    if not isinstance(instance, get_tenant_model()):
        return
    if instance.auto_drop_schema and schema_exists(instance.schema_name):
        instance._drop_schema(True)