# Generated by Django 4.2.6 on 2024-06-05 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0007_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlysalary',
            name='paid_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
