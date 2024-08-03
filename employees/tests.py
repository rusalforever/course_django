from django.test import TestCase
from .models import Employee

class EmployeeTestCase(TestCase):
    
    def setUp(self):
        Employee.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        Employee.objects.create(first_name="Jane", last_name="Smith", email="jane@example.com")
    
    def test_employee_names(self):
        john = Employee.objects.get(first_name="John")
        jane = Employee.objects.get(first_name="Jane")
        self.assertEqual(john.last_name, 'Doe')
        self.assertEqual(jane.last_name, 'Smith')
