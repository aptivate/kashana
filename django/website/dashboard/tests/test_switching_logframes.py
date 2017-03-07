from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.test.client import RequestFactory

import mock
import pytest

from logframe.models import LogFrame

from ..views import SwitchLogframes


@mock.patch('dashboard.views.get_object_or_404', new=mock.Mock(return_value=mock.Mock(spec=LogFrame, slug='test')))
def test_switch_logframes_sets_user_last_viewed_logframe_to_new_logframe():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()

    SwitchLogframes.as_view()(request)

    assert 'test' == request.user.preferences.last_viewed_logframe.slug


@mock.patch('dashboard.views.get_object_or_404', new=mock.Mock(spec=LogFrame, return_value=mock.Mock(slug='test', organization=mock.Mock(slug='org_test'))))
def test_switch_logframes_containts_instruction_to_redirect_to_dashboard():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchLogframes.as_view()(request)
    assert reverse('logframe-dashboard', kwargs={'slug': 'test', 'org_slug': 'org_test'}) == response['Location']


@pytest.mark.django_db
def test_switch_logframe_with_invalid_id_raises_404():
    data = {'logframe': '-1'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    with pytest.raises(Http404):
        SwitchLogframes.as_view()(request)
