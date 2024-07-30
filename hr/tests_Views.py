from django.test import TestCase, Client
from django.urls import reverse
from hr.models import Employee, Position, Department
from django.contrib.auth import get_user_model

class EmployeeProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name='Developer')
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.employee = Employee.objects.create(
            first_name='John', last_name='Doe', position=self.position, user=self.user
        )
        self.profile_url = reverse('hr:employee_profile', args=[self.employee.pk])

    def test_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hr/employee_profile.html')
        self.assertEqual(response.context['employee'], self.employee)

class EmployeeDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name='Developer')
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.employee = Employee.objects.create(
            first_name='John', last_name='Doe', position=self.position, user=self.user
        )
        self.delete_url = reverse('hr:employee_delete', args=[self.employee.pk])

    def test_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

class EmployeeUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name='Developer')
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.employee = Employee.objects.create(
            first_name='John', last_name='Doe', position=self.position, user=self.user
        )
        self.update_url = reverse('hr:employee_update', args=[self.employee.pk])

    def test_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.update_url, {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'position': self.position.pk
        })
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, 'Jane')
        self.assertEqual(self.employee.last_name, 'Smith')
