from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LoginTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_login_view(self):
        # Test the login view
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_success(self):
        # Test successful login
        login_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), data=login_data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('user_landing'))

    def test_login_failure(self):
        # Test unsuccessful login
        login_data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), data=login_data)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertContains(response, 'Invalid username or password')

    def test_logout_view(self):
        # Test logout view
        response = self.client.get(reverse('logout_view'))
        self.assertRedirects(response, reverse('login'))
