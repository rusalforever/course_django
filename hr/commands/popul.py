import os
import random
from django.contrib.auth.hashers import make_password
from hr.models import Employee, Position, Department
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_django.settings")
import django
django.setup()

fake = Faker()

def populate():
    # Generate Departments
    departments = [Department(name=fake.unique.company()) for _ in range(4)]
    Department.objects.bulk_create(departments)

    # Refresh departments from the database to get their IDs
    departments = list(Department.objects.all())

    # Generate Positions
    positions = [Position(
        title=fake.job(),
        department=random.choice(departments),
        is_active=True
    ) for _ in range(10)]
    Position.objects.bulk_create(positions)

    positions = list(Position.objects.all())

    employees = []
    for _ in range(50):  # Adjust the number of employees as needed
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = fake.unique.user_name()
        email = username + '@kmail.com'
        password = make_password(fake.password())
        hire_date = fake.date_between(start_date='-5y', end_date='today')
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
        position = random.choice(positions)
        employees.append(Employee(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            hire_date=hire_date,
            birth_date=birth_date,
            position=position
        ))

    try:
        Employee.objects.bulk_create(employees)
        print('Data successfully generated!')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    populate()
