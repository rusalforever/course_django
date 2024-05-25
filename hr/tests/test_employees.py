from django.contrib.messages import get_messages
from django.test import (
    Client,
    TestCase,
)
from django.urls import reverse

from hr.models import Employee
from hr.tests.factories import (
    EmployeeFactory,
    PositionFactory,
)


class EmployeeListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employees = EmployeeFactory.create_batch(10)
        self.client.force_login(self.employees[0])
        self.url = reverse('hr:employee_list')

    def test_access_employee_list(self):
        # response = self.client.get(self.url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_employee_list_content(self):
        # response = self.client.get(self.url, )
        response = self.client.get(self.url )
        self.assertTrue('employees' in response.context)
        self.assertEqual(len(response.context['employees']), 10)

    def test_employee_search(self):
        search_query = self.employees[0].first_name
        # response = self.client.get(f'{self.url}?search={search_query}')
        response = self.client.get(f'{self.url}?search={search_query}')
        self.assertTrue(len(response.context['employees']), 1)
        self.assertEqual(response.context['employees'][0].first_name, search_query)


class EmployeeCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.non_admin_user = EmployeeFactory(is_staff=False, is_superuser=False)
        self.employee = EmployeeFactory()
        self.position = PositionFactory()
        self.url = reverse('hr:employee_create')

    def test_successful_employee_creation(self):
        self.client.force_login(self.admin_user)
        username = 'newuser'
        employee_data = {
            'username': username,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id,
        }
        # response = self.client.post(self.url, employee_data)
        response = self.client.post(self.url, employee_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Employee.objects.filter(username=username).exists())

    def test_create_employee_by_non_admin(self):
        self.client.force_login(self.non_admin_user)
        username = 'newuser'
        employee_data = {
            'username': username,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id,
        }
        response = self.client.post(self.url, employee_data)
        # response = self.client.post(self.url, employee_data)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(username=username).exists())

    def test_successful_employee_creation_message(self):
        self.client.force_login(self.admin_user)
        username = 'newuser'
        employee_data = {
            'username': username,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'position': self.position.id,
        }
        # response = self.client.post(self.url, employee_data)
        response = self.client.post(self.url, employee_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Працівника успішно створено.')


class EmployeeProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = EmployeeFactory(is_staff=True, is_superuser=True)
        self.url = reverse('hr:employee_profile', kwargs={'pk': self.employee.pk})
        self.client.force_login(self.employee)

    def test_access_employee_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_profile.html')
        self.assertEqual(response.context['employee'], self.employee)


class EmployeeDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = EmployeeFactory()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.url = reverse('hr:employee_delete', kwargs={'pk': self.employee.pk})
        self.client.force_login(self.admin_user)

    def test_delete_employee(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())


class EmployeeUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.employee = EmployeeFactory()
        self.admin_user = EmployeeFactory(is_staff=True, is_superuser=True)
        self.url = reverse('hr:employee_update', kwargs={'pk': self.employee.pk})
        self.client.force_login(self.admin_user)
        self.position = PositionFactory()

    def test_update_employee(self):
        new_first_name = 'UpdatedName'
        employee_data = {
            'username': self.employee.username,
            'first_name': new_first_name,
            'last_name': self.employee.last_name,
            'email': self.employee.email,
            'position': self.position.id,
        }
        response = self.client.post(self.url, employee_data)
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.first_name, new_first_name)
