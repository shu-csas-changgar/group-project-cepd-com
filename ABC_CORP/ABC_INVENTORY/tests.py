from django.test import TestCase
from django.contrib.auth import get_user_model

class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com','firstname','lastname','password'
        )
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.firstName, 'firstname')
        self.assertEqual(super_user.lastName, 'lastname')
        self.assertEqual(super_user.is_superuser,True)
        self.assertEqual(super_user.is_staff,True)
        self.assertEqual(super_user.is_active,True)
        self.assertEqual(super_user.is_admin,True)
        self.assertEqual(str(super_user), 'firstname'+' '+'lastname')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            'testuser@super.com','firstname','lastname','password',
            is_superuser=False
        )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            email='testuser@super.com',firstName='firstname',lastName='lastname',password='password',
            is_staff=False
        )

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com','firstname','lastname','password'
        )
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.firstName, 'firstname')
        self.assertEqual(user.lastName, 'lastname')
        self.assertEqual(user.is_superuser,False)
        self.assertEqual(user.is_staff,True)
        self.assertEqual(user.is_active,True)
        self.assertEqual(user.is_admin,False)
        self.assertEqual(str(user), 'firstname'+' '+'lastname')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
            email ='',firstName='firstname',lastName='lastname',password='password',
            is_superuser=False
        )

