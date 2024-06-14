from django.core.management.base import BaseCommand
import random
from faker import Faker
from hr.models import Employee, Position, Department

fake = Faker()

class Command(BaseCommand):
    help = 'Generate random Department, Position, and Employee instances'

    def handle(self, *args, **kwargs):
        departments = []
        for _ in range(5):
            department = Department.objects.create(name=fake.company())
            departments.append(department)

        positions = []
        for _ in range(10):
            department = random.choice(departments)
            position = Position.objects.create(
                title=fake.job(),
                department=department,
            )
            positions.append(position)

        common_password = 'fau_1'

        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            position = random.choice(positions)

            hashed_password = common_password

            Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                position=position,
                password=hashed_password,
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated Departments, Positions, and Employees'))
