from django.core.management.base import BaseCommand
from hr.models import Employee


class Command(BaseCommand):
    help = 'Set "paid" as True for all employees'  # noqa: A003

    def handle(self, *args, **kwargs):
        Employee.objects.filter(is_active=False).update(is_active=True)
