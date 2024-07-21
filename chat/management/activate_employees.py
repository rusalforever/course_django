from django.core.management.base import BaseCommand
from your_app.models import Employee

class Command(BaseCommand):
    help = 'Activate all employee accounts'

    def handle(self, *args, **kwargs):
        Employee.objects.update(status='active')
        self.stdout.write(self.style.SUCCESS('Successfully activated all employees'))