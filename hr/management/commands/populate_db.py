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
            department = Department.objects.create(name=fake.unique.company())
            departments.append(department)

        positions = []
        for _ in range(10):
            department = random.choice(departments)
            monthly_rate = random.randint(10000, 30000)  # Generating random monthly rate
            position = Position.objects.create(
                title=fake.job(),
                department=department,
                is_active=True,
                monthly_rate=monthly_rate,  # Setting monthly rate
            )
            positions.append(position)

        hr_department = random.choice(departments)
        hr_monthly_rate = random.randint(10000, 30000)  # Generating random monthly rate for HR Manager
        hr_position = Position.objects.create(
            title='HR Manager',
            department=hr_department,
            is_active=True,
            is_manager=True,
            monthly_rate=hr_monthly_rate,  # Setting monthly rate for HR Manager
        )
        positions.append(hr_position)

        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.unique.user_name()  # Ensure unique username
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
