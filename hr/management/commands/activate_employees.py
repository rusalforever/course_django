from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    help = 'Activate all employees'

    def handle(self, *args, **kwargs):
        employees = Employee.objects.all()
        updated_count = employees.update(is_active=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully activated {updated_count} employees'))
