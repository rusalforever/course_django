from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from hr.models import Employee, Position
from hr.tests.factories import (
    EmployeeFactory,
    PositionFactory, DepartmentFactory,
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
        self.user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.department = DepartmentFactory()
        self.positions = PositionFactory.create_batch(10, department=self.department)
        self.client.force_authenticate(user=self.user)

    def test_get_position_list(self):
        response = self.client.get(reverse('api-hr:position-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_position(self):
        data = {
            'title': 'new_position',
            'department': self.department.pk,
            'is_manager': False,
            'is_active': True,
            'job_description': 'new position',
            'monthly_rate': 10000
        }
        response = self.client.post(reverse('api-hr:position-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Position.objects.count(), len(self.positions) + 1)

    def test_update_position(self):
        position = self.positions[0]
        data = {'title': 'updated_position'}
        response = self.client.patch(reverse('api-hr:position-detail', kwargs={'pk': position.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        position.refresh_from_db()
        self.assertEqual(position.title, 'updated_position')

    def test_retrieve_position(self):
        position = self.positions[0]
        response = self.client.get(reverse('api-hr:position-detail', kwargs={'pk': position.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], position.title)

    def test_delete_position(self):
        position = self.positions[0]
        response = self.client.delete(reverse('api-hr:position-detail', kwargs={'pk': position.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Position.objects.filter(pk=position.pk).exists())
