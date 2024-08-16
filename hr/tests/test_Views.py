from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from hr.models import Employee

User = get_user_model()

class EmployeeViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            password='password'
        )
        self.client.force_authenticate(user=self.user)
        self.employee = Employee.objects.create_user(
            username='john_doe',
            first_name='John',
            last_name='Doe',
            password='password',
            phone_number='1234567890'
        )
        self.url_list = reverse('employee-list')
        self.url_detail = reverse('employee-detail', args=[self.employee.id])

    def test_employee_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data[0])

    def test_employee_create(self):
        data = {
            'username': 'jane_doe',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'password',
            'phone_number': '0987654321'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.latest('id').username, 'jane_doe')

    def test_employee_delete(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

    def test_employee_retrieve(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.employee.first_name)

    def test_employee_update(self):
        data = {
            'first_name': 'Johnathan',
            'last_name': 'Smith',
            'phone_number': '1112223333'
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, data['first_name'])
        self.assertEqual(self.employee.last_name, data['last_name'])
        self.assertEqual(self.employee.phone_number, data['phone_number'])

