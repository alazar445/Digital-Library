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
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(UserProfile.objects.filter(user=user, gender='male', education_status='student').exists())
        self.assertContains(response, 'Registration successful')

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
