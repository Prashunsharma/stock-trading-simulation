# Generated by Django 5.1.1 on 2024-11-14 15:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0008_alter_userstock_custom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstock',
            name='balance',
            field=models.FloatField(default=1000000, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='userstock',
            name='custom_id',
            field=models.PositiveIntegerField(default=6493, unique=True),
        ),
    ]
