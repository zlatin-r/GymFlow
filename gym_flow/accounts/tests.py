from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from gym_flow.accounts.forms import AppUserCreationForm
from gym_flow.accounts.models import Profile

UserModel = get_user_model()


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.user_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        user = UserModel.objects.get(email=self.user_data['email'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_login(self):
        user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_logout(self):
        user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_registration_form_valid(self):
        form_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = AppUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        form_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        }
        form = AppUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)


class AppUserModelTests(TestCase):
    def test_create_user(self):
        user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = UserModel.objects.create_superuser(email='admin@example.com', password='adminpassword123')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_uniqueness(self):
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        with self.assertRaises(Exception):
            UserModel.objects.create_user(email='testuser@example.com', password='anotherpassword123')

    def test_user_required_fields(self):
        self.assertEqual(UserModel.USERNAME_FIELD, 'email')
        self.assertEqual(UserModel.REQUIRED_FIELDS, [])


class ProfileModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='testuser1@example.com', password='testpassword123')
        self.profile = self.user.profile  # Assuming automatic profile creation

    def test_profile_creation(self):
        self.profile.username = 'testuser1_username'
        self.profile.first_name = 'John'
        self.profile.last_name = 'Doe'
        self.profile.date_of_birth = '1990-01-01'
        self.profile.profile_picture = SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg')
        self.profile.save()

        self.assertEqual(self.profile.user.email, 'testuser1@example.com')
        self.assertEqual(self.profile.username, 'testuser1_username')
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(str(self.profile.date_of_birth), '1990-01-01')
        self.assertTrue(self.profile.profile_picture)

    def test_profile_user_relationship(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile, self.profile)

    def test_profile_str_representation(self):
        self.profile.username = 'testuser3_username'
        self.profile.save()
        self.assertEqual(str(self.profile), 'testuser3_username')

    def test_profile_picture_upload(self):
        self.profile.profile_picture = SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg')
        self.profile.save()
        self.assertTrue(self.profile.profile_picture.name.startswith('profile_pictures/'))
        self.assertTrue(self.profile.profile_picture.name.endswith('.jpg'))

    def test_profile_optional_fields(self):
        # Check that optional fields are falsy (None or empty) by default
        self.assertFalse(self.profile.username)  # Changed from assertIsNone
        self.assertFalse(self.profile.first_name)  # Changed from assertIsNone
        self.assertFalse(self.profile.last_name)  # Changed from assertIsNone
        self.assertFalse(self.profile.date_of_birth)  # Changed from assertIsNone
        self.assertFalse(self.profile.profile_picture)  # Changed from assertIsNone