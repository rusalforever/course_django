from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from faker import Faker
from hr.models import Department, Position

fake = Faker()

class PositionViewSetTest(APITestCase):

    def setUp(self):
        self.department = Department.objects.create(name=fake.company())
        self.position = Position.objects.create(name=fake.job(), department=self.department)
        self.url_list = reverse('position-list')
        self.url_detail = reverse('position-detail', args=[self.position.id])
        self.new_position_data = {
            'name': fake.job(),
            'department': self.department.id
        }

    def test_position_create(self):
        response = self.client.post(self.url_list, self.new_position_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Position.objects.count(), 2)
        self.assertEqual(Position.objects.latest('id').name, self.new_position_data['name'])

    def test_position_retrieve(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.position.name)

    def test_position_update(self):
        updated_data = {
            'name': fake.job(),
            'department': self.department.id
        }
        response = self.client.put(self.url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, updated_data['name'])

    def test_position_delete(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Position.objects.filter(id=self.position.id).exists())
