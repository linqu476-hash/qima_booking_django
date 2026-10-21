from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='BookingRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('queued', 'Queued'), ('running', 'Running'), ('done', 'Completed'), ('failed', 'Failed')], db_index=True, default='queued', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('booking_file', models.FileField(blank=True, upload_to='runs/%Y/%m/%d/booking/')),
                ('booking_list_file', models.FileField(blank=True, upload_to='runs/%Y/%m/%d/list/')),
                ('technical_info_file', models.FileField(blank=True, upload_to='runs/%Y/%m/%d/technical/')),
                ('error_message', models.TextField(blank=True)),
                ('log_text', models.TextField(blank=True)),
                ('workspace', models.CharField(blank=True, max_length=500)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
