from django.core.management.base import BaseCommand
from django.utils import timezone

from hr.models import Employee


class Command(BaseCommand):
    help = 'Set "paid" as True for all MonthlySalary instances where month_year is the current month'  # noqa: A003

    def handle(self, *args, **kwargs):
        employees = Employee.objects.all()
        for employee in employees:
            if not employee.is_active:
                employee.is_active = True
                employee.save()
                print(f"employee {employee.id} / {employee.username} set to {employee.is_active}")