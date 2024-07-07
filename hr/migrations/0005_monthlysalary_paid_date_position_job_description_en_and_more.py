# Generated by Django 4.2.6 on 2024-05-03 19:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_monthlysalary_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlysalary',
            name='paid_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='job_description_en',
            field=models.CharField(default='', max_length=500, null=True, verbose_name='Job Description'),
        ),
        migrations.AddField(
            model_name='position',
            name='job_description_uk',
            field=models.CharField(default='', max_length=500, null=True, verbose_name='Job Description'),
        ),
        migrations.AddField(
            model_name='position',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='position',
            name='title_uk',
            field=models.CharField(max_length=200, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='position',
            name='job_description',
            field=models.CharField(default='', max_length=500, verbose_name='Job Description'),
        ),
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
    ]
