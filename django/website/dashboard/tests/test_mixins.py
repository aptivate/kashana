from django.contrib.sessions.middleware import SessionMiddleware
from django.http.response import Http404
from django.test.client import RequestFactory

from django_dynamic_fixture import G
import mock
import pytest

from logframe.models import LogFrame

from ..mixins import OverviewMixin


@pytest.mark.django_db
def test_get_logframe_returns_new_logframe_if_none_exists():
    LogFrame.objects.all().delete()

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(session={})
    overview_mixin.kwargs = {}
    log_frame = overview_mixin.get_logframe()

    assert log_frame == LogFrame.objects.get()


@pytest.mark.django_db
def test_get_logframe_returns_existing_logframe_where_one_exists():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(session={})
    overview_mixin.kwargs = {}
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_returns_first_logframe_by_default():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(session={})
    overview_mixin.kwargs = {}
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_current_logframe_slug_from_session():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]
    request.session['current_logframe'] = expected_log_frame.slug

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_current_logframe_slug_from_kwargs():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_current_logframe_slug_from_kwargs_in_preference_to_session():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    unused_logframe, expected_log_frame = G(LogFrame, n=2)
    request.session['current_logframe'] = unused_logframe.slug

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_current_logframe_set_when_not_in_session_but_slug_in_kwargs():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame.slug == overview_mixin.request.session['current_logframe']


@pytest.mark.django_db
def test_current_logframe_set_when_different_in_session_and_slug_in_kwargs():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    unused_logframe, expected_log_frame = G(LogFrame, n=2)
    request.session['current_logframe'] = unused_logframe.slug

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame.slug == overview_mixin.request.session['current_logframe']


@pytest.mark.django_db
def test_get_logframe_stores_logframe_id_in_session():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    overview_mixin.get_logframe()

    assert expected_log_frame.slug == request.session['current_logframe']


@pytest.mark.django_db
def test_get_logframe_raises_404_when_given_invalid_logframe_id():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    request.session['current_logframe'] = '!not)a(slug'

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    with pytest.raises(Http404):
        overview_mixin.get_logframe()


@pytest.mark.django_db
def test_get_logframe_doesnt_set_logframe_id_in_session_if_present():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    logframe = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    request.session = mock.MagicMock(
        __getitem__=lambda _, __: logframe.slug,
        __contains__=lambda _, __: True,
        __setitem__=mock.Mock()
    )

    overview_mixin.get_logframe()

    assert not request.session.__setitem__.called
