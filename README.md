# models.py

from django.core.exceptions import ValidationError
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    tax_code = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk and Company.objects.exists():
            raise ValidationError('There can be only one Company instance')
        return super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Employee(models.Model):
    # ... other fields ...
    phone_number = models.CharField(max_length=20)
    # Add other necessary fields and methods

class Position(models.Model):
    # ... other fields ...
    job_description = models.TextField()
    # Add other necessary fields and methods

# admin.py

from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone_number')
    # Add other configurations if necessary
