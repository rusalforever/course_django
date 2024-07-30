from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from hr.models import Position, Employee, Department
from django.contrib.auth import get_user_model

class PositionViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='admin', password='password')
        self.client.login(username='admin', password='password')
        self.department = Department.objects.create(name='Тестовий відділ')
        self.position = Position.objects.create(name='Manager',  department_id=31)
        self.list_url = reverse('api-hr:position-list')
        self.detail_url = reverse('api-hr:position-detail', args=[self.position.pk])

    def test_list_positions(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_position(self):
        response = self.client.post(self.list_url, {'name': 'Developer', 'department': self.department.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Position.objects.count(), 2)

    def test_retrieve_position(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Manager')

    def test_update_position(self):
        response = self.client.patch(self.detail_url, {'name': 'Team Lead'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, 'Team Lead')

    def test_delete_position(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Position.objects.filter(pk=self.position.pk).exists())
