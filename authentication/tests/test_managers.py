from rest_framework.test import APITestCase
from authentication.models import User


class TestManager(APITestCase):

    def test_creates_user(self):
        user = User.objects.create_user('testuser', 'testuser@email.com', 'password1234!')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertEqual(user.username, 'testuser')
        self.assertFalse(user.is_staff)

    def test_creates_super_user(self):
        user = User.objects.create_superuser('testuser', 'superuser@email.com', 'password1234!')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'superuser@email.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='', email='testuser@email.com', password='password1234!')

    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set' ):
            User.objects.create_user(username="", email='testuser@email.com', password='Password123!@')


    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username='testuser', email='', password='password1234!')

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set' ):
            User.objects.create_user(username="testuser", email='', password='Password123!@')

    def test_cant_create_superuser_with_no_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='testuser', email='testuser@email.com', password='Password123!@', is_staff=False,)

    
    def test_cant_create_super_user_with_no_super_user_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.' ):
            User.objects.create_superuser(username='testuser', email='testuser@email.com', password='Password123!@', is_superuser=False,)

        