from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AdminLoginTestCase(TestCase):
    def setUp(self):
        # Create a test admin user
        self.admin_username = 'admin'
        self.admin_password = 'securepassword123'
        self.admin_user = User.objects.create_user(
            username=self.admin_username,
            password=self.admin_password,
            is_staff=True
        )
    
    def test_login_with_correct_credentials(self):
        # Try to login with correct username and password
        response = self.client.post(reverse('admin_login'), {
            'username': self.admin_username,
            'password': self.admin_password
        })
        # You can check for redirect (302) or success message
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_wrong_username(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'wronguser',
            'password': self.admin_password
        })
        self.assertEqual(response.status_code, 200)  # stays on login page
        self.assertContains(response, "Invalid username or password.")  # adjust depending on your template message
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_with_wrong_password(self):
        response = self.client.post(reverse('admin_login'), {
            'username': self.admin_username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_with_empty_fields(self):
        response = self.client.post(reverse('admin_login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")
        self.assertFalse(response.wsgi_request.user.is_authenticated)
