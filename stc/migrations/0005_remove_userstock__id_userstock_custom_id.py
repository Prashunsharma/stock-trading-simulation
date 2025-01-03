# Generated by Django 5.1.1 on 2024-11-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0004_userstock__id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstock',
            name='_id',
        ),
        migrations.AddField(
            model_name='userstock',
            name='custom_id',
            field=models.PositiveIntegerField(default=8300, unique=True),
        ),
    ]
