# Generated by Django 5.0.7 on 2024-08-15 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0009_position_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='name',
        ),
    ]
