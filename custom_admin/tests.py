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
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages



class CustomAdminViewsTests(TestCase):

    def setUp(self):
        # Create a staff user who can access admin pages
        self.staff_user = User.objects.create_user(
            username='staff', password='staffpass', is_staff=True
        )
        # Create a normal user who should NOT access admin pages
        self.normal_user = User.objects.create_user(
            username='normal', password='normalpass', is_staff=False
        )

    def test_dashboard_requires_login(self):
        """
        If a user tries to access the admin dashboard without logging in,
        they should be redirected to the login page.
        """
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(
            response,
            '/admin_login/?next=' + reverse('admin_dashboard')
        )

    def test_dashboard_loads_for_logged_in_staff(self):
        """
        A logged-in staff user should be able to see the admin dashboard.
        """
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('admin_dashboard'))

        # Should load successfully
        self.assertEqual(response.status_code, 200)
        # Should use the correct HTML template
        self.assertTemplateUsed(response, 'custom_admin/admin_panel.html')

    def test_login_invalid_credentials(self):
        """
        If someone enters the wrong username or password,
        they should see an error message on the login page.
        """
        response = self.client.post(reverse('admin_login'), {
            'username': 'wrong',
            'password': 'wrongpass'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_admin/login.html')

        # Check if the error message is present
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("Invalid username or password" in str(m) for m in messages)
        )

    def test_login_non_staff_user(self):
        """
        If a normal user tries to login, they should see an authorization error.
        """
        response = self.client.post(reverse('admin_login'), {
            'username': 'normal',
            'password': 'normalpass'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'custom_admin/login.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any("not authorized" in str(m) for m in messages)
        )

    def test_login_staff_redirects_to_dashboard(self):
        """
        A valid staff user should be logged in and redirected to the dashboard.
        """
        response = self.client.post(reverse('admin_login'), {
            'username': 'staff',
            'password': 'staffpass'
        })

        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_logout_redirects_to_login_and_protects_dashboard(self):
        """
        After logging out, the user should be redirected to login page.
        And trying to access dashboard again should also redirect to login.
        """
        self.client.login(username='staff', password='staffpass')

        # Now logout
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('admin_login'))

        # Try to access dashboard again (should fail)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(
            response,
            '/admin_login/?next=' + reverse('admin_dashboard')
        )
