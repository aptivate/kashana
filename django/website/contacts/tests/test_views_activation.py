from contacts.views.activation import ResetPassword
from django.conf import settings


def test_reset_password_subject_contains_site_name():
    assert '{0}: password recovery'.format(settings.SITE_NAME) == ResetPassword().get_subject()
