from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.test.client import RequestFactory

import mock
import pytest

from ..views import SwitchLogframes


@mock.patch('dashboard.views.LogFrame.objects.get', new=mock.Mock(return_value=mock.Mock(slug='test')))
def test_switch_logframes_sets_user_last_viewed_logframe_to_new_logframe():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()

    SwitchLogframes.as_view()(request)

    assert 'test' == request.user.preferences.last_viewed_logframe.slug


@mock.patch('dashboard.views.LogFrame.objects.get', new=mock.Mock(return_value=mock.Mock(slug='test')))
def test_switch_logframes_contains_instruction_to_redirect_to_dashboard():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchLogframes.as_view()(request)
    assert reverse('logframe-dashboard', kwargs={'slug': 'test'}) == response['Location']


@pytest.mark.django_db
def test_switch_logframe_with_invalid_id_redirects_to_create_logframe_view():
    data = {'logframe': '-1'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchLogframes.as_view()(request)
    assert reverse('create-logframe') == response['Location']
