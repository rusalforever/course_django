import random

from django.core.management.base import BaseCommand
from faker import Faker

from hr.models import Department, Employee, Position


fake = Faker()


class Command(BaseCommand):
    help = 'Generate random Department, Position, and Employee instances'

    def handle(self, *args, **kwargs):
        # Generate Departments
        departments = []
        for _ in range(5):
            department = Department.objects.create(name=fake.unique.company())
            departments.append(department)

        # Generate Positions
        positions = []
        for _ in range(10):
            department = random.choice(departments)
            position = Position.objects.create(
                title=fake.job(),
                department=department,
                is_active=True,
            )
            positions.append(position)

        # Generate Employees
        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.unique.user_name()
            email = username + '@example.com'
            password = 'password123'  # You might want to generate random passwords here
            employee = Employee.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
                position=random.choice(positions),
            )

        self.stdout.write(self.style.SUCCESS('Data successfully generated!'))
