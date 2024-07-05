from django.core.management.base import BaseCommand
import random
from faker import Faker
from hr.models import Employee, Position, Department, Company

fake = Faker()

class Command(BaseCommand):
    help = 'Generate random Company, Department, Position, and Employee instances'

    def handle(self, *args, **kwargs):
        if not Company.objects.exists():
            Company.objects.create(
                name=fake.company(),
                address=fake.address(),
                email=fake.email(),
                tax_code=fake.unique.ean(length=13)
            )

        departments = []
        for _ in range(5):
            department = Department.objects.create(name=fake.unique.company())
            departments.append(department)

        positions = []
        for _ in range(10):
            department = random.choice(departments)
            position = Position.objects.create(
                title=fake.job(),
                department=department,
                job_description=fake.text(max_nb_chars=200),
                is_active=True,
                monthly_rate=random.randint(3000, 10000)
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
                phone_number=fake.phone_number()
            )

        self.stdout.write(self.style.SUCCESS('Data successfully generated!'))
