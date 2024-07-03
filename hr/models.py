from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=200)
    parent_department = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_manager:
            existing_manager = Position.objects.filter(
                department=self.department, is_manager=True
            ).exclude(pk=self.pk).exists()  # Exclude the current instance

            if existing_manager:
                raise ValidationError(
                    f"Manager already exists in the {self.department.name} department."
                )
        super(Position, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Employee(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    is_manager = models.BooleanField(default=False)
    hire_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=200, null=True, blank=True)
    position = models.ForeignKey(
        "Position", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
