from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.test.client import RequestFactory

import mock
import pytest

from ..views import SwitchLogframes


@mock.patch('dashboard.views.get_object_or_404', new=mock.Mock(return_value=mock.Mock(slug='test')))
def test_switch_logframes_sets_session_id_to_new_logframe_id():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = mock.MagicMock(__setitem__=mock.Mock())
    SwitchLogframes.as_view()(request)

    request.session.__setitem__.assert_called_with('current_logframe', 'test')


@mock.patch('dashboard.views.get_object_or_404', new=mock.Mock(return_value=mock.Mock(slug='test')))
def test_switch_logframes_containts_instruction_to_redirect_to_dashboard():
    data = {'logframe': '2'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    response = SwitchLogframes.as_view()(request)
    assert reverse('logframe-dashboard', kwargs={'slug': 'test'}) == response['Location']


@pytest.mark.django_db
def test_switch_logframe_with_invalid_id_raises_404():
    data = {'logframe': '-1'}

    request = RequestFactory().post('/', data)
    request.user = mock.Mock()
    request.session = {}

    with pytest.raises(Http404):
        SwitchLogframes.as_view()(request)
