import pytest

from django.contrib.auth.models import Permission, Group, ContentType
from django.core.exceptions import ObjectDoesNotExist

from contacts.group_permissions import GroupPermissions


def get_expected_permissions(model, codenames):
    content_type = ContentType.objects.get_for_model(model)
    expected_permissions = []
    for name in codenames:
        perm, _ = Permission.objects.get_or_create(name=name,
                                                   codename=name,
                                                   content_type=content_type)
        expected_permissions.append(perm)
    return expected_permissions


def create_groups_with_permissions(codenames):
    g1, _ = Group.objects.get_or_create(name="Test Group 1")
    g2, _ = Group.objects.get_or_create(name="Test Group 2")

    gp = GroupPermissions()
    with gp.groups(g1, g2):
        gp.add_permissions(Group, *codenames)

    return (g1, g2)


@pytest.mark.django_db
def test_add_perms():
    any_model = Group  # for example
    codenames = ['a_do_stuff', 'b_do_more_stuff']

    expected_permissions = get_expected_permissions(any_model, codenames)
    g1, g2 = create_groups_with_permissions(codenames)

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


def test_logging_happens_when_verbose_is_true(capsys):
    gp = GroupPermissions()
    gp.verbose = True

    gp.log('Hello World')

    output, _ = capsys.readouterr()

    assert 'Hello World\n' == output


def test_logging_doesnt_happen_when_verbose_is_false(capsys):
    gp = GroupPermissions()
    gp.verbose = False

    gp.log('Hello World')

    output, _ = capsys.readouterr()

    assert '' == output


@pytest.mark.django_db
def test_deleting_all_group_permissions():
    any_model = Group  # for example
    codenames = ['i_can_do_stuff', 'u_can_do_more_stuff']

    get_expected_permissions(any_model, codenames)
    g1, g2 = create_groups_with_permissions(codenames)

    gp = GroupPermissions()

    gp.delete_all_group_permissions()

    assert list(g1.permissions.all()) == []
    assert list(g2.permissions.all()) == []
