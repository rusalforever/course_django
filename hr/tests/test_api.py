from django.test import TestCase, Client
from django.urls import reverse
from .models import Employee, Position
from rest_framework.test import APITestCase, APIClient

# EmployeeProfileView Test
class EmployeeProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = Employee.objects.create(name='Hlieb Ovsiienko', position='Developer')

    def test_employee_profile_view(self):
        response = self.client.get(reverse('employee_profile', args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_profile.html')
        self.assertContains(response, self.employee.name)

# EmployeeDeleteView Test
class EmployeeDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = Employee.objects.create(name='Hlieb Ovsiienko', position='Developer')

    def test_employee_delete_view(self):
        response = self.client.post(reverse('employee_delete', args=[self.employee.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('employee_list'))
        self.assertFalse(Employee.objects.filter(id=self.employee.id).exists())

# EmployeeUpdateView Test
class EmployeeUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = Employee.objects.create(name='Hlieb Ovsiienko', position='Developer')

    def test_employee_update_view(self):
        response = self.client.post(reverse('employee_update', args=[self.employee.id]), {
            'name': 'Hlieb Ovsiienko',
            'position': 'Manager'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('employee_detail', args=[self.employee.id]))
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'Hlieb Ovsiienko')
        self.assertEqual(self.employee.position, 'Manager')

# PositionViewSet Test
class PositionViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.position = Position.objects.create(name='Developer')

    def test_list_positions(self):
        response = self.client.get(reverse('position-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_position(self):
        response = self.client.post(reverse('position-list'), {'name': 'Manager'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Position.objects.count(), 2)

    def test_update_position(self):
        response = self.client.patch(reverse('position-detail', args=[self.position.id]), {'name': 'Senior Developer'})
        self.assertEqual(response.status_code, 200)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, 'Senior Developer')

    def test_delete_position(self):
        response = self.client.delete(reverse('position-detail', args=[self.position.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Position.objects.filter(id=self.position.id).exists())

    def test_get_position_list(self):
        # Your code to test position list view
        pass  # Replace with actual test code

    def test_create_position(self):
        # Your code to test position creation
        pass  # Replace with actual test code

    def test_update_position(self):
        # Your code to test position update
        pass  # Replace with actual test code

    def test_delete_position(self):
        # Your code to test position deletion
        pass  # Replace with actual test code
