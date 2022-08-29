# Generated by Django 3.2.13 on 2022-08-29 19:01

import core.models.files
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20220829_2055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='files',
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(blank=True, upload_to=core.models.files.Files.group_based_upload_to, verbose_name='files required')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]