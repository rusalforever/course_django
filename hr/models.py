from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Company(models.Model):
    name = models.CharField(max_length=200)
    addresss = models.CharField(max_length=200)
    email = models.EmailField()
    tax_code = models.CharField(max_length=200)
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Забезпечення того, що існує лише один інстанс
        if not self.pk and Company.objects.exists():
            raise ValidationError('There can be only one Company instance.')
        return super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name




class Department(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_department:
            existing_department = Department.objects.filter(department=self.company, is_manager=True).exists()
            if existing_department:
                raise ValidationError(f"Department already exists in the {self.company.name} .")
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_manager:
            existing_manager = Position.objects.filter(department=self.department, is_manager=True).exists()
            if existing_manager:
                raise ValidationError(f"Manager already exists in the {self.department.name} department.")
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Employee(AbstractUser):
    hire_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)
