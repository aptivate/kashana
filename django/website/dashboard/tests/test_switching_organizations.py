from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

import mock
from organizations.models import Organization
import pytest

from ..views import SwitchOrganizations


@mock.patch('dashboard.views.Organization.objects.get', new=mock.Mock(return_value=mock.Mock(spec=Organization, slug='test')))
def test_switch_organizations_sets_user_last_viewed_organization_to_new_organization():
    data = {'organization': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()

    SwitchOrganizations.as_view()(request)

    assert 'test' == request.user.preferences.last_viewed_organization.slug


@mock.patch('dashboard.views.Organization.objects.get', new=mock.Mock(spec=Organization, return_value=mock.Mock(slug='org_test')))
def test_switch_organizations_containts_instruction_to_redirect_to_dashboard():
    data = {'organization': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchOrganizations.as_view()(request)
    assert reverse('org-dashboard', kwargs={'org_slug': 'org_test'}) == response['Location']


@pytest.mark.django_db
def test_switch_organization_with_invalid_id_redirects_to_create_organization():
    data = {'organization': '-1'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchOrganizations.as_view()(request)
    assert reverse('organization_create') == response['Location']
