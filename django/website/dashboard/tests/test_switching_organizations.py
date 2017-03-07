from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.test.client import RequestFactory

import mock
from organizations.models import Organization
import pytest

from ..views import SwitchOrganizations


@mock.patch('dashboard.views.get_object_or_404', new=mock.Mock(return_value=mock.Mock(spec=Organization, slug='test')))
def test_switch_logframes_sets_user_last_viewed_logframe_to_new_logframe():
    data = {'organization': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()

    SwitchOrganizations.as_view()(request)

    assert 'test' == request.user.preferences.last_viewed_organization.slug


@mock.patch('dashboard.views.get_object_or_404', new=mock.Mock(spec=Organization, return_value=mock.Mock(slug='org_test')))
def test_switch_logframes_containts_instruction_to_redirect_to_dashboard():
    data = {'organization': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchOrganizations.as_view()(request)
    assert reverse('org-dashboard', kwargs={'org_slug': 'org_test'}) == response['Location']


@pytest.mark.django_db
def test_switch_logframe_with_invalid_id_raises_404():
    data = {'organization': '-1'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    with pytest.raises(Http404):
        SwitchOrganizations.as_view()(request)
