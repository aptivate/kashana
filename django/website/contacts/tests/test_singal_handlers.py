from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test.client import RequestFactory

from django_dynamic_fixture import G
import pytest
from registration.signals import user_activated


@pytest.mark.django_db
def test_permission_to_create_organizations_granted_on_user_activation():
    User = get_user_model()
    user = G(User)
    create_orgs_permission = Permission.objects.get(codename='add_organization')
    request = RequestFactory().get('/')

    user_activated.send(None, user=user, request=request)

    # Reload the user instance
    user = User.objects.get(pk=user.pk)

    assert create_orgs_permission in user.user_permissions.all()
