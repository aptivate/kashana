from django.test import TestCase
from contacts.group_permissions import GroupPermissions
from django.contrib.auth.models import Group
from contacts.models import User, PictureUploadHandler
from .factories import UserFactory


class UserTests(TestCase):
    def setUp(self):
        self.user = UserFactory(first_name='Fake', last_name='Name')

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Name, Fake")

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "Fake")


class UserManagerTests(TestCase):
    email = 'fake@aptivate.org'
    password = 'badpass'

    def test_create_user_basic(self):
        User.objects.create_user(self.email, self.password)
        # NB If there's more than one this will fail
        user = User.objects.get(business_email=self.email)
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_user_advanced(self):
        User.objects.create_user(self.email,
                                 self.password,
                                 is_active=False,
                                 is_staff=True)
        user = User.objects.get(business_email=self.email)
        assert not user.is_active
        assert user.is_staff
        assert not user.is_superuser

    def test_create_super_user(self):
        User.objects.create_superuser(self.email, self.password)
        user = User.objects.get(business_email=self.email)
        assert user.is_active
        assert user.is_staff
        assert user.is_superuser


##################
# pytest tests
##################

create_picture_upload_handler = PictureUploadHandler('pictures')


def test_create_picture_upload_handler_with_both_names():
    u = User(first_name='Ime', last_name='Priimek',
             business_email='fake@aptivate.org')
    handler = create_picture_upload_handler
    assert handler(u, 'me.jpg') == 'pictures/Priimek_Ime_me.jpg'


def test_create_picture_upload_handler_with_missing_first_name():
    u = User(last_name='Priimek', business_email='fake@aptivate.org')
    handler = create_picture_upload_handler
    assert handler(u, 'me.jpg') == 'pictures/Priimek_me.jpg'


def test_create_picture_upload_handler_with_missing_last_name():
    u = User(first_name='Ime', business_email='fake@aptivate.org')
    handler = create_picture_upload_handler
    assert handler(u, 'me.jpg') == 'pictures/Ime_me.jpg'


def test_create_picture_upload_handler_with_missing_names():
    u = User(business_email='fake@aptivate.org')
    handler = create_picture_upload_handler
    assert handler(u, 'me.jpg') == 'pictures/fake@aptivate.org_me.jpg'
