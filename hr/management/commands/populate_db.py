from django.core.management.base import BaseCommand
import random
from faker import Faker
from hr.models import Employee, Position, Department

fake = Faker()


class Command(BaseCommand):
    help = 'Generate random Employee, Position and Department instances'

    def handle(self, *args, **kwargs):
        departments = []
        for i in range(5):
            department = Department.objects.create(name=fake.unique.company())
            departments.append(department)

        positions = []
        for j in range(10):
            position = Position.objects.create(title=fake.job(), department=department)
            positions.append(position)

        for e in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.unique.user_name()
            email = username + '@example.com'
            password = 'password123'
            employee = Employee.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
                position=random.choice(positions)
            )
        self.stdout.write(self.style.SUCCESS('Data successfully generated!'))