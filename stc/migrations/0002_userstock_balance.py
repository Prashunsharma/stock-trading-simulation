# Generated by Django 5.1.1 on 2024-11-14 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstock',
            name='balance',
            field=models.BigIntegerField(default=1000000),
        ),
    ]
