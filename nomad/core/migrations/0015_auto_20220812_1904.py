# Generated by Django 3.2.13 on 2022-08-12 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20220812_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklocation',
            name='city',
            field=models.CharField(blank=True, editable=False, help_text='this field is auto-completed', max_length=100, null=True, verbose_name='city'),
        ),
        migrations.AddField(
            model_name='worklocation',
            name='department',
            field=models.PositiveIntegerField(blank=True, editable=False, help_text='this field is autocompleted', null=True, verbose_name='department'),
        ),
        migrations.AddField(
            model_name='worklocation',
            name='department_name',
            field=models.CharField(blank=True, editable=False, help_text='this field is autocompleted', max_length=100, null=True, verbose_name='department name'),
        ),
        migrations.AddField(
            model_name='worklocation',
            name='region',
            field=models.CharField(blank=True, editable=False, help_text='this field is autocompleted', max_length=100, null=True, verbose_name='region'),
        ),
    ]
