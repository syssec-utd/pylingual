from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('notifications', '0001_initial')]
    operations = [migrations.AlterField(model_name='notification', name='notification_status', field=models.CharField(choices=[('read', 'Read'), ('unread', 'Unread'), ('deleted', 'Deleted')], max_length=20))]