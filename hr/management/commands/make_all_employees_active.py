from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    help = 'Make all employees active.'

    def handle(self, *args, **kwargs):
        employees = Employee.objects.all()
        employees.update(is_active=True)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set "is_active" to True for all ({employees.count()}) employees.',
            ),
        )
