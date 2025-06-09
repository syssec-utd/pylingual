from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name='UserOTPData', fields=[('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('secret', models.CharField(blank=True, max_length=96, verbose_name='16 character, base32 encoded random string.')), ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='otp_data', to=settings.AUTH_USER_MODEL, verbose_name='User'))], options={'verbose_name': 'User OTP data', 'verbose_name_plural': 'Users OTP data'})]