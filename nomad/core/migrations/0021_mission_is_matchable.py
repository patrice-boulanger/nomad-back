# Generated by Django 3.2.13 on 2022-08-24 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20220824_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='is_matchable',
            field=models.BooleanField(default=False, verbose_name='is matchable'),
        ),
    ]
