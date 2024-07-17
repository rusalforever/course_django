import os
import random

from django.core.management.base import BaseCommand
from faker import Faker

from hr.models import Department, Employee, Position, Company

fake = Faker()

class Command(BaseCommand):
    help = 'Generate random Department, Position, and Employee instances'

    def handle(self, *args, **kwargs):
        company_logo_path = os.path.join('staticfiles', 'img', 'logot.png')
        company = Company.objects.create(
            name=fake.company(),
            address=fake.address(),
            email=fake.email(),
            tax_code=fake.bothify(text='???-########'),
            logo=company_logo_path
        )
        self.stdout.write(self.style.SUCCESS(f'Company {company.name} created with logo {company_logo_path}'))

        departments = []
        for _ in range(5):
            department = Department.objects.create(
                name=fake.unique.company(),
            )
            departments.append(department)

        positions = []
        for _ in range(10):
            department = random.choice(departments)
            is_manager = not Position.objects.filter(department=department, is_manager=True).exists()
            position = Position.objects.create(
                title=fake.job(),
                department=department,
                is_manager=is_manager,
                is_active=True,
                job_description=fake.text(),
                monthly_rate=random.randint(200, 1000),
            )
            positions.append(position)

        for _ in range(100):
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
                position=random.choice(positions),
                phone_number=fake.phone_number(),
                avatar=fake.image_url(width=200, height=200),
                cv=fake.file_name(category='document', extension='pdf'),
            )

        self.stdout.write(self.style.SUCCESS('Data successfully generated!'))
