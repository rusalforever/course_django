from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from typing import Optional

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)
    parent_department = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs) -> None:
        if self.is_manager:
            existing_manager = Position.objects.filter(
                department=self.department, is_manager=True
            ).exists()
            if existing_manager:
                raise ValidationError(
                    f"Manager already exists in the {self.department.name} department."
                )
        super(Position, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

class Employee(AbstractUser):
    hire_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return self.username

    @property
    def department(self) -> Optional[Department]:
        return self.position.department if self.position else None
