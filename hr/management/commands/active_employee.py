from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    help = "Make all Employee active"

    def handle(self, *args, **options):
        Employee.objects.all().update(is_active=True)
        self.stdout.write(self.style.SUCCESS(f"All Employees are active'"))
