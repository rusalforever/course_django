from django.core.exceptions import ValidationError
from django.db import models

# Company Model
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    tax_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ця частина для забезпечення того, що буде існувати лише один інстанс
        if not self.pk and Company.objects.exists():
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)

# Employee Model
class Employee(models.Model):
    # ... existing fields ...
    phone_number = models.CharField(max_length=20)
    # Це модель саме 

# Position Model
class Position(models.Model):
    # ... existing fields ...
    job_description = models.TextField()
    # Це модель більше про позицію персоналу