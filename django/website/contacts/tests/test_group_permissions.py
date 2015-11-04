import pytest

from django.contrib.auth.models import Permission, Group, ContentType
from django.core.exceptions import ObjectDoesNotExist

from contacts.group_permissions import GroupPermissions


@pytest.mark.django_db
def test_add_perms():
    g1, _ = Group.objects.get_or_create(name="Test Group 1")
    g2, _ = Group.objects.get_or_create(name="Test Group 2")
    any_model = Group  # for example
    content_type = ContentType.objects.get_for_model(any_model)
    codenames = ['a_do_stuff', 'b_do_more_stuff']
    expected_permissions = []
    for name in codenames:
        perm, _ = Permission.objects.get_or_create(name=name,
                                                   codename=name,
                                                   content_type=content_type)
        expected_permissions.append(perm)

    gp = GroupPermissions()
    with gp.groups(g1, g2):
        gp.add_permissions(any_model, *codenames)
    assert list(g1.permissions.all()) == expected_permissions
    assert list(g2.permissions.all()) == expected_permissions


@pytest.mark.django_db
def test_add_nonexistent_perms():
    g1, _ = Group.objects.get_or_create(name="Test Group 1")
    g2, _ = Group.objects.get_or_create(name="Test Group 2")
    any_model = Group  # for example
    codenames = ['a_do_stuff', 'b_do_more_stuff']

    gp = GroupPermissions()
    with gp.groups(g1, g2):
        try:
            gp.add_permissions(any_model, *codenames)
            pytest.fail("This should raise an ObjectDoesNotExist exception", False)
        except ObjectDoesNotExist:
            pass
