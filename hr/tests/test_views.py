from django.test import TestCase, Client
from django.urls import reverse
from .models import Employee
from django.contrib.auth.models import User

class EmployeeProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile_url = reverse('employee_profile', kwargs={'pk': self.user.pk})

    def test_employee_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employee_profile.html')