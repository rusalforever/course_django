# Generated by Django 5.0.2 on 2024-05-19 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logo/'),
        ),
    ]
