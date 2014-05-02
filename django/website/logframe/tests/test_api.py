import pytest
import mock

from django_dynamic_fixture import G
from django.contrib.auth.models import Permission
from contacts.models import User
from contacts.group_permissions import GroupPermissions
from ..api import CanEditOrReadOnly


@pytest.mark.django_db
def test_default_user_can_read_data():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    u1 = G(User)

    request = mock.Mock(method="GET", user=u1)
    perm_obj = CanEditOrReadOnly()
    assert perm_obj.has_object_permission(request, None, None) is True


@pytest.mark.django_db
def test_default_user_can_not_change_data():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    u1 = G(User)

    request = mock.Mock(method="POST", user=u1)
    perm_obj = CanEditOrReadOnly()
    assert perm_obj.has_object_permission(request, None, None) is False


@pytest.mark.django_db
def test_editor_can_change_data():
    gp = GroupPermissions()
    gp.setup_groups_and_permissions()
    u1 = G(User)
    edit_perm = Permission.objects.get(codename='edit_logframe')
    u1.user_permissions.add(edit_perm)

    request = mock.Mock(method="POST", user=u1)
    perm_obj = CanEditOrReadOnly()
    assert perm_obj.has_object_permission(request, None, None) is True
