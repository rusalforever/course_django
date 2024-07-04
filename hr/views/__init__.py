import os
import django
import random
from django.utils.crypto import get_random_string
from faker import Faker
from hr.models import Employee, Position, Department

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_django.settings")
django.setup()

fake = Faker()

def populate():
    departments = [Department(name=fake.unique.company()) for _ in range(4)]
    Department.objects.bulk_create(departments)

    positions = [Position(
        title=fake.job(),
        department=random.choice(departments),
        is_active=True
    ) for _ in range(10)]
    Position.objects.bulk_create(positions)

    employees = [Employee(
        username=fake.unique.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=f'{username}@kmail.com',
        password=get_random_string(),
        hire_date=fake.date_between(start_date='-5y', end_date='today'),
        birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
        position=random.choice(positions)
    ) for _ in range(10)]
    Employee.objects.bulk_create(employees)

if __name__ == "__main__":
    populate()
  
  if __name__ == "__main__":
      populate()
