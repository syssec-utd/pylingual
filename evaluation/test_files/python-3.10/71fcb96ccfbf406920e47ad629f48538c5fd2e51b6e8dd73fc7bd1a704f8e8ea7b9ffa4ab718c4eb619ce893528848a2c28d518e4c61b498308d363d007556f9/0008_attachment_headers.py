from django.db import migrations
import jsonfield.fields

class Migration(migrations.Migration):
    dependencies = [('post_office', '0007_auto_20170731_1342')]
    operations = [migrations.AddField(model_name='attachment', name='headers', field=jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Headers'))]