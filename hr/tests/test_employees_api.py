from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from hr.models import Employee, Position
from hr.tests.factories import (
    EmployeeFactory,
    PositionFactory,
)


class EmployeeAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Employee.objects.create_user(username='testuser', password='testpassword', email='test@gmail.com')
        self.position = PositionFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_employee_list(self):
        response = self.client.get(reverse('api-hr:employee-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        data = {
            'username': 'newemployee',
            'first_name': 'Test',
            'last_name': 'Employee',
            'email': 'test@employee.com',
            'position': self.position.pk,
        }
        response = self.client.post(reverse('api-hr:employee-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_employee(self):
        employee = EmployeeFactory(position=self.position)
        data = {'first_name': 'Updated Name'}
        response = self.client.patch(reverse('api-hr:employee-detail', kwargs={'pk': employee.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee(self):
        employee = EmployeeFactory(position=self.position)
        response = self.client.delete(reverse('api-hr:employee-detail', kwargs={'pk': employee.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_employee(self):
        response = self.client.get(reverse('api-hr:employee-list'), {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PositionViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = EmployeeFactory(is_staff=True, is_superuser=True)  # Адміністратор
        self.client.force_authenticate(user=self.user)
        self.position = PositionFactory()

    def test_get_position_list(self):
        response = self.client.get(reverse('api-hr:position-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)

    def test_create_position(self):
        data = {
            'title': 'New Position',
            'department': self.position.department.pk,
            'is_manager': False,
            'is_active': True,
            'job_description': 'Job description here',
            'monthly_rate': 5000
        }
        response = self.client.post(reverse('api-hr:position-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Position.objects.count(), 2)
        self.assertEqual(Position.objects.get(id=response.data['id']).title, 'New Position')

    def test_update_position(self):
        data = {
            'title': 'Updated Position',
            'department': self.position.department.pk,
            'is_manager': self.position.is_manager,
            'is_active': self.position.is_active,
            'job_description': 'Updated job description',
            'monthly_rate': self.position.monthly_rate
        }
        response = self.client.put(reverse('api-hr:position-detail', kwargs={'pk': self.position.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.title, 'Updated Position')

    def test_partial_update_position(self):
        data = {'title': 'Partially Updated Position'}
        response = self.client.patch(reverse('api-hr:position-detail', kwargs={'pk': self.position.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.title, 'Partially Updated Position')

    def test_delete_position(self):
        response = self.client.delete(reverse('api-hr:position-detail', kwargs={'pk': self.position.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Position.objects.count(), 0)
