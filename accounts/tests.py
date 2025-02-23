from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegisterViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test1@test.com'
        )

    def test_register_page(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_success(self):
        form_data = {
            'username': 'testuser2',
            'email': 'test2@test.com',
            'password1': 'testpassword2',
            'password2': 'testpassword2',
        }
        response = self.client.post(reverse('accounts:register'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

    def test_register_fail(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword2',
            'email': 'test1@test.com'
        }
        response = self.client.post(reverse('accounts:register'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertIn("password2", response.context['form'].errors)
        self.assertIn('username', response.context['form'].errors)
        self.assertIn('email', response.context['form'].errors)

    def test_redirect_if_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bookings:home'))


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_redirect_if_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bookings:home'))


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
