from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from contacts.models import UserPreferences
import mock
import pytest
from logframe.models import LogFrame

from ..views import SwitchLogframes


@mock.patch('dashboard.views.LogFrame.objects.get', new=mock.Mock(return_value=mock.Mock(spec=LogFrame, slug='test', organization=mock.Mock(slug="test-org"))))
def test_switch_logframes_sets_user_last_viewed_logframe_to_new_logframe():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()

    SwitchLogframes.as_view()(request)

    assert 'test' == request.user.preferences.last_viewed_logframe.slug


@mock.patch('dashboard.views.LogFrame.objects.get', new=mock.Mock(return_value=mock.Mock(spec=LogFrame, slug='test', organization=mock.Mock(slug="test-org"))))
def test_switch_logframes_contains_instruction_to_redirect_to_dashboard():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock(preferences=mock.Mock())
    request.session = {}

    response = SwitchLogframes.as_view()(request)
    assert reverse('logframe-dashboard', kwargs={'org_slug':'test-org', 'slug': 'test'}) == response['Location']


@pytest.mark.django_db
def test_switch_logframe_with_invalid_id_redirects_to_create_logframe_view():
    data = {'logframe': '-1'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchLogframes.as_view()(request)
    assert reverse('create-logframe') == response['Location']
