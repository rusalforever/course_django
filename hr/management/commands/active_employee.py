from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        employees = Employee.objects.filter(is_active=False)
        employees.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully found (not active) employees and replaced them with active ones {employees.count()}.',
            ),
        )
