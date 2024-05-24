import random
from django.core.management.base import BaseCommand
from faker import Faker
from hr.models import Department, Employee, Position

fake = Faker()

class Command(BaseCommand):
    help = 'Generate random Department, Position, and Employee instances'

    def handle(self, *args, **kwargs):
        # Генерация департаментов
        departments = []
        for _ in range(5):
            department = Department.objects.create(name=fake.unique.company())
            departments.append(department)

        # Генерация позиций
        positions = []
        for department in departments:
            for _ in range(10):
                position = Position.objects.create(
                    title=fake.job(),
                    department=department,
                    is_active=True,
                )
                positions.append(position)

        # Генерация сотрудников
        for _ in range(100):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.unique.user_name()
            email = username + '@example.com'
            password = 'password123'
            position = random.choice(positions)
            employee = Employee.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                hire_date=fake.date_between(start_date='-5y', end_date='today'),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
                position=position,
                department=position.department,
            )

        self.stdout.write(self.style.SUCCESS('Данные успешно сгенерированы!'))
