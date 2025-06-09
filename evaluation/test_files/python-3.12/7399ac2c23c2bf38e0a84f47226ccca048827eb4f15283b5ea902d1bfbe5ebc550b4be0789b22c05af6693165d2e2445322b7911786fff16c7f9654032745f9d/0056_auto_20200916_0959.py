from django.db import migrations
from mayan.apps.storage.classes import DefinedStorage
from mayan.apps.documents import settings
STORAGE_NAME_DOCUMENT_IMAGE = 'documents__documentimagecache'

def code_purge_and_delete_file_cache(apps, schema_editor):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    try:
        cache = Cache.objects.get(defined_storage_name=STORAGE_NAME_DOCUMENT_IMAGE)
    except Cache.DoesNotExist:
        return
    else:
        try:
            DefinedStorage.get(name=cache.defined_storage_name)
        except KeyError:
            '\n            Unknown or deleted storage. Must not be purged otherwise only\n            the database data will be erased but the actual storage files\n            will remain.\n            '
        else:
            for partition in cache.partitions.all():
                for parition_file in partition.files.all():
                    parition_file.delete()
        cache.delete()

def code_purge_and_delete_file_cache_reverse(apps, schema_editor):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    setting_document_cache_maximum_size = getattr(settings, 'setting_document_cache_maximum_size', None)
    if setting_document_cache_maximum_size:
        document_cache_maximum_size = setting_document_cache_maximum_size.value
    else:
        document_cache_maximum_size = 500 * 2 ** 20
    Cache.objects.create(defined_storage_name=STORAGE_NAME_DOCUMENT_IMAGE, maximum_size=document_cache_maximum_size)

class Migration(migrations.Migration):
    dependencies = [('documents', '0055_auto_20200814_0626'), ('file_caching', '0006_auto_20200322_0626')]
    operations = [migrations.RunPython(code=code_purge_and_delete_file_cache, reverse_code=code_purge_and_delete_file_cache_reverse)]