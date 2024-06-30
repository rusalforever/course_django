from django.core.management.base import BaseCommand
from hr.models import Employee

class Command(BaseCommand):
    help = 'Activate all employees'

    def handle(self, *args, **kwargs):
        employees_updated = Employee.objects.update(is_active=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully activated {employees_updated} employees'))
