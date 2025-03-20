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
        self.assertEqual(response.status_code, 302)  # Check if redirects after successful registration
        self.assertRedirects(response, self.home_url)

        # Check if the user was created
        user = UserModel.objects.get(email=self.user_data['email'])
        self.assertEqual(user.email, self.user_data['email'])

        # Check if the user is logged in after registration
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_login(self):
        # Create a user first
        user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')

        # Attempt to login
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)  # Check if redirects after successful login
        self.assertRedirects(response, self.home_url)

        # Check if the user is logged in
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_logout(self):
        # Create a user and log them in
        user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.client.login(email='testuser@example.com', password='testpassword123')

        # Attempt to logout using POST request
        response = self.client.post(self.logout_url)  # Use POST instead of GET
        self.assertEqual(response.status_code, 302)  # Check if redirects after successful logout
        self.assertRedirects(response, self.home_url)

        # Check if the user is logged out
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
        self.assertIn('password2', form.errors)  # Check if the error is in password2 field


class AppUserModelTests(TestCase):
    def test_create_user(self):
        # Create a user
        user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')

        # Check if the user was created successfully
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        # Create a superuser
        superuser = UserModel.objects.create_superuser(email='admin@example.com', password='adminpassword123')

        # Check if the superuser was created successfully
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_uniqueness(self):
        # Create a user with a specific email
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')

        # Try to create another user with the same email
        with self.assertRaises(Exception):  # Should raise an integrity error
            UserModel.objects.create_user(email='testuser@example.com', password='anotherpassword123')

    def test_user_required_fields(self):
        # Check the USERNAME_FIELD and REQUIRED_FIELDS
        self.assertEqual(UserModel.USERNAME_FIELD, 'email')
        self.assertEqual(UserModel.REQUIRED_FIELDS, [])


class ProfileModelTests(TestCase):
    def setUp(self):
        # Create a user and a profile for testing
        self.user = UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.profile = Profile.objects.create(
            user=self.user,
            username='testuser',
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            profile_picture=SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg')
        )

    def test_profile_creation(self):
        # Check if the profile was created successfully
        self.assertEqual(self.profile.user.email, 'testuser@example.com')
        self.assertEqual(self.profile.username, 'testuser')
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(str(self.profile.date_of_birth), '1990-01-01')
        self.assertTrue(self.profile.profile_picture)

    def test_profile_user_relationship(self):
        # Check the one-to-one relationship between Profile and UserModel
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.user.profile, self.profile)

    def test_profile_str_representation(self):
        # Test the __str__ method of the Profile model
        self.assertEqual(str(self.profile), 'testuser')

    def test_profile_picture_upload(self):
        # Test the profile picture upload
        self.assertTrue(self.profile.profile_picture.name.startswith('profile_pictures/'))
        self.assertTrue(self.profile.profile_picture.name.endswith('.jpg'))

    def test_profile_optional_fields(self):
        # Test optional fields (blank=True, null=True)
        profile = Profile.objects.create(user=self.user)
        self.assertIsNone(profile.username)
        self.assertIsNone(profile.first_name)
        self.assertIsNone(profile.last_name)
        self.assertIsNone(profile.date_of_birth)
        self.assertIsNone(profile.profile_picture)
