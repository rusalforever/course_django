from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from faker import Faker
from hr.models import Department, Position, Employee

fake = Faker()

class EmployeeProfileViewTest(APITestCase):

    def setUp(self):
        self.department = Department.objects.create(name=fake.company())
        self.position = Position.objects.create(name=fake.job(), department=self.department)
        self.employee = Employee.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            position=self.position
        )
        self.url = reverse('employee-profile', args=[self.employee.id])

    def test_employee_profile_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.employee.first_name)
        self.assertEqual(response.data['last_name'], self.employee.last_name)
        self.assertEqual(response.data['email'], self.employee.email)
        self.assertEqual(response.data['phone_number'], self.employee.phone_number)

class EmployeeDeleteViewTest(APITestCase):

    def setUp(self):
        self.department = Department.objects.create(name=fake.company())
        self.position = Position.objects.create(name=fake.job(), department=self.department)
        self.employee = Employee.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            position=self.position
        )
        self.url = reverse('employee-delete', args=[self.employee.id])

    def test_employee_delete_view(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

class EmployeeUpdateViewTest(APITestCase):

    def setUp(self):
        self.department = Department.objects.create(name=fake.company())
        self.position = Position.objects.create(name=fake.job(), department=self.department)
        self.employee = Employee.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            position=self.position
        )
        self.url = reverse('employee-update', args=[self.employee.id])
        self.new_data = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'position': self.position.id
        }

    def test_employee_update_view(self):
        response = self.client.put(self.url, self.new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, self.new_data['first_name'])
        self.assertEqual(self.employee.last_name, self.new_data['last_name'])
        self.assertEqual(self.employee.email, self.new_data['email'])
        self.assertEqual(self.employee.phone_number, self.new_data['phone_number'])
