from faker import Faker
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_django.settings")

import django
django.setup()

from hr.models import Employee


fake = Faker()

for i in range(100):
    employee = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        username=fake.user_name(),
        hire_date=fake.date(),
        birth_date=fake.date(),
    )
    employee.save()