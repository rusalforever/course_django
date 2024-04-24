# Generated by Django 5.0.4 on 2024-04-24 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0003_department_company_alter_department_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='job_description',
            field=models.CharField(default=1, max_length=1300),
            preserve_default=False,
        ),
    ]
