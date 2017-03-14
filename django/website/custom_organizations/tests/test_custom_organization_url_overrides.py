from django.core.urlresolvers import reverse

import pytest
from django_dynamic_fixture import G, N
from organizations.models import Organization

from ..views import OrganizationEdit, OrganizationDelete


def test_edit_organization_can_be_accessed_with_slug():
    org_edit_url = reverse('organization_edit', args=['test-org'])
    assert '/orgs/test-org/edit/' == org_edit_url


def test_delete_organization_can_be_accessed_with_slug():
    org_edit_url = reverse('organization_delete', args=['test-org'])
    assert '/orgs/test-org/delete/' == org_edit_url


@pytest.mark.django_db
def test_edit_organization_can_get_object_using_slug():
    expected_org = G(Organization)
    expected_org.slug = 'test'
    expected_org.save()

    edit_view = OrganizationEdit()
    edit_view.kwargs = {'org_slug': 'test'}

    actual_org = edit_view.get_object()

    assert expected_org == actual_org


@pytest.mark.django_db
def test_delete_organization_can_get_object_using_slug():
    expected_org = G(Organization)
    expected_org.slug = 'test'
    expected_org.save()

    delete_view = OrganizationDelete()
    delete_view.kwargs = {'org_slug': 'test'}

    actual_org = delete_view.get_object()

    assert expected_org == actual_org
