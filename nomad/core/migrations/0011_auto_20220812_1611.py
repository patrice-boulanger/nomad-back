# Generated by Django 3.2.13 on 2022-08-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availability',
            name='from_dt',
            field=models.DateTimeField(verbose_name='start'),
        ),
        migrations.AlterField(
            model_name='availability',
            name='to_dt',
            field=models.DateTimeField(verbose_name='end'),
        ),
    ]