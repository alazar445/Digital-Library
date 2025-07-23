from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile

# Create your tests here.

class RegistrationTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_data = {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'gender': 'male',
            'education_status': 'student',
        }

    def test_valid_registration_creates_user_and_profile(self):
        response = self.client.post(self.register_url, self.valid_data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(UserProfile.objects.filter(user=user, gender='male', education_status='student').exists())

    def test_duplicate_username(self):
        User.objects.create_user(username='testuser', email='other@example.com', password='pass')
        data = self.valid_data.copy()
        response = self.client.post(self.register_url, data)
        self.assertContains(response, 'Username already exists')

    def test_duplicate_email(self):
        User.objects.create_user(username='otheruser', email='testuser@example.com', password='pass')
        data = self.valid_data.copy()
        response = self.client.post(self.register_url, data)
        self.assertContains(response, 'Email already exists')

    def test_password_mismatch(self):
        data = self.valid_data.copy()
        data['confirm_password'] = 'differentpass'
        response = self.client.post(self.register_url, data)
        self.assertContains(response, 'Passwords do not match')

class RegistrationIntegrationTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_data = {
            'full_name': 'Integration User',
            'email': 'integration@example.com',
            'username': 'integrationuser',
            'password': 'integrationpass',
            'confirm_password': 'integrationpass',
            'gender': 'female',
            'education_status': 'teacher',
        }

    def test_registration_form_renders(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Your Account')
        self.assertContains(response, 'Full Name')
        self.assertContains(response, 'Email Address')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'Confirm Password')
        self.assertContains(response, 'Gender')
        self.assertContains(response, 'Education Status')

    def test_successful_registration_flow(self):
        response = self.client.post(self.register_url, self.valid_data, follow=False)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='integrationuser').exists())
        user = User.objects.get(username='integrationuser')
        self.assertTrue(UserProfile.objects.filter(user=user, gender='female', education_status='teacher').exists())

    def test_registration_duplicate_username_integration(self):
        User.objects.create_user(username='integrationuser', email='other@email.com', password='pass')
        data = self.valid_data.copy()
        response = self.client.post(self.register_url, data)
        self.assertContains(response, 'Username already exists')

    def test_registration_duplicate_email_integration(self):
        User.objects.create_user(username='otheruser', email='integration@example.com', password='pass')
        data = self.valid_data.copy()
        response = self.client.post(self.register_url, data)
        self.assertContains(response, 'Email already exists')

    def test_registration_password_mismatch_integration(self):
        data = self.valid_data.copy()
        data['confirm_password'] = 'notthesame'
        response = self.client.post(self.register_url, data)
        self.assertContains(response, 'Passwords do not match')
