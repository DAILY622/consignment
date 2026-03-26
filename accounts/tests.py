from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Str0ngPass!',
            'password2': 'Str0ngPass!',
            'first_name': 'New',
            'last_name': 'User',
            'phone': '07700900000',
        })
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(self.url, {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password': 'Str0ngPass!',
            'password2': 'WrongPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')

    def test_register_short_password(self):
        response = self.client.post(self.url, {
            'username': 'newuser3',
            'email': 'newuser3@example.com',
            'password': 'short',
            'password2': 'short',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'at least 8 characters')

    def test_register_invalid_email(self):
        response = self.client.post(self.url, {
            'username': 'newuser4',
            'email': 'not-an-email',
            'password': 'Str0ngPass!',
            'password2': 'Str0ngPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'valid email address')

    def test_register_invalid_phone(self):
        response = self.client.post(self.url, {
            'username': 'newuser5',
            'email': 'newuser5@example.com',
            'password': 'Str0ngPass!',
            'password2': 'Str0ngPass!',
            'phone': '12345',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'valid UK phone number')

    def test_register_duplicate_username(self):
        User.objects.create_user(username='existing', email='existing@example.com', password='pass1234')
        response = self.client.post(self.url, {
            'username': 'existing',
            'email': 'other@example.com',
            'password': 'Str0ngPass!',
            'password2': 'Str0ngPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')

    def test_register_duplicate_email(self):
        User.objects.create_user(username='user1', email='taken@example.com', password='pass1234')
        response = self.client.post(self.url, {
            'username': 'user2',
            'email': 'taken@example.com',
            'password': 'Str0ngPass!',
            'password2': 'Str0ngPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')


class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='testpass123',
            phone='07700900001',
        )
        self.client.login(username='profileuser', password='testpass123')
        self.url = reverse('profile')

    def test_profile_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_profile_update_success(self):
        response = self.client.post(self.url, {
            'action': 'update_profile',
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'phone': '07700900002',
            'address': '1 Test St',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_profile_update_invalid_email(self):
        response = self.client.post(self.url, {
            'action': 'update_profile',
            'email': 'not-valid',
            'phone': '',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        # Email should NOT have changed
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'profile@example.com')

    def test_profile_update_invalid_phone(self):
        response = self.client.post(self.url, {
            'action': 'update_profile',
            'email': 'profile@example.com',
            'phone': '99999',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '07700900001')

    def test_change_password_success(self):
        response = self.client.post(self.url, {
            'action': 'change_password',
            'current_password': 'testpass123',
            'new_password': 'NewPass456!',
            'confirm_password': 'NewPass456!',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))

    def test_change_password_wrong_current(self):
        response = self.client.post(self.url, {
            'action': 'change_password',
            'current_password': 'wrongpassword',
            'new_password': 'NewPass456!',
            'confirm_password': 'NewPass456!',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_change_password_mismatch(self):
        response = self.client.post(self.url, {
            'action': 'change_password',
            'current_password': 'testpass123',
            'new_password': 'NewPass456!',
            'confirm_password': 'Mismatch789!',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('testpass123'))

    def test_delete_account_success(self):
        response = self.client.post(self.url, {
            'action': 'delete_account',
            'confirm_delete_password': 'testpass123',
        })
        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)
        self.assertFalse(User.objects.filter(username='profileuser').exists())

    def test_delete_account_wrong_password(self):
        response = self.client.post(self.url, {
            'action': 'delete_account',
            'confirm_delete_password': 'wrongpassword',
        })
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username='profileuser').exists())


class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')

    def test_contact_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_contact_missing_fields(self):
        response = self.client.post(self.url, {
            'name': 'Test User',
            'email': 'test@example.com',
            # missing subject and message
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'required fields')


class UserModelTests(TestCase):
    def test_is_admin_for_superuser(self):
        user = User.objects.create_superuser(username='su', email='su@example.com', password='pass1234')
        self.assertTrue(user.is_admin())

    def test_is_admin_for_admin_role(self):
        user = User.objects.create_user(username='adm', email='adm@example.com', password='pass1234', role='admin')
        self.assertTrue(user.is_admin())

    def test_is_driver(self):
        user = User.objects.create_user(username='drv', email='drv@example.com', password='pass1234', role='driver')
        self.assertTrue(user.is_driver())
        self.assertFalse(user.is_admin())

    def test_str_representation(self):
        user = User.objects.create_user(username='strtest', email='s@example.com', password='pass1234', role='user')
        self.assertIn('strtest', str(user))
        self.assertIn('Customer', str(user))
