# Generated by Django 3.2.13 on 2022-08-12 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220812_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_dt', models.DateTimeField()),
                ('to_dt', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Availability timeslot',
                'verbose_name_plural': 'Availability timeslots',
                'ordering': ('from_dt',),
            },
        ),
    ]
