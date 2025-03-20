from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from gym_flow.accounts.forms import AppUserCreationForm

UserModel = get_user_model()


# Authentication Tests
class AuthTests(TestCase):
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

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        user = UserModel.objects.get(email=self.user_data['email'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_user_success(self):
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_user_success(self):
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertFalse('_auth_user_id' in self.client.session)


# View Tests
class ViewTests(TestCase):
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

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertContains(response, 'Register')
        self.assertIsInstance(response.context['form'], AppUserCreationForm)

    def test_register_view_post_valid(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        user = UserModel.objects.get(email=self.user_data['email'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.profile)
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_register_view_post_invalid(self):
        invalid_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        }
        response = self.client.post(self.register_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFalse(UserModel.objects.filter(email='testuser@example.com').exists())
        self.assertContains(response, 'The two password fields didn’t match')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'Login')

    def test_login_view_post_valid(self):
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        login_data = {
            'username': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(self.client.session.get('_auth_user_id'))

    def test_login_view_post_invalid(self):
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        invalid_data = {
            'username': 'testuser@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertContains(response, 'testuser@example.com')  # Check that the form re-renders with username
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_logout_view_post(self):
        UserModel.objects.create_user(email='testuser@example.com', password='testpassword123')
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(self.client.session.get('_auth_user_id'))


# Form Tests
class FormTests(TestCase):
    def test_app_user_creation_form_valid(self):
        form_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = AppUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_app_user_creation_form_invalid_password_mismatch(self):
        form_data = {
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
        }
        form = AppUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_app_user_creation_form_invalid_email(self):
        form_data = {
            'email': 'invalid-email',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = AppUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_app_user_creation_form_missing_fields(self):
        form_data = {
            'email': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = AppUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['This field is required.'])


# Model Tests
class UserModelTests(TestCase):
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
        self.profile = self.user.profile

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
        self.assertFalse(self.profile.username)
        self.assertFalse(self.profile.first_name)
        self.assertFalse(self.profile.last_name)
        self.assertFalse(self.profile.date_of_birth)
        self.assertFalse(self.profile.profile_picture)
