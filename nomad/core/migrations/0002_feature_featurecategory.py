# Generated by Django 3.2.13 on 2022-08-10 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
                ('multiple_choices', models.BooleanField(default=False, verbose_name='multiple choices')),
            ],
            options={
                'verbose_name': 'Features category',
                'verbose_name_plural': 'Features categories',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300, unique=True, verbose_name='description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='features', to='core.featurecategory')),
            ],
        ),
    ]
