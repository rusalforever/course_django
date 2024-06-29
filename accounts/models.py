from django.core.exceptions import ValidationError
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    tax_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensuring that only one instance exists
        if not self.pk and Company.objects.exists():
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)

class Employee(models.Model):
    # ... other fields ...
    phone_number = models.CharField(max_length=20)

class Position(models.Model):
    # ... other fields ...
    job_description = models.TextField()