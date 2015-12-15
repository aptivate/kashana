from django.contrib.sessions.middleware import SessionMiddleware
from django.http.response import Http404
from django.test.client import RequestFactory

from django_dynamic_fixture import G, N
import mock
import pytest

from logframe.models import LogFrame

from ..mixins import OverviewMixin, update_current_logframe


@pytest.mark.django_db
def test_get_logframe_returns_new_logframe_if_none_exists():
    LogFrame.objects.all().delete()

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=mock.Mock(last_viewed_logframe=None))
    overview_mixin.kwargs = {}

    log_frame = overview_mixin.get_logframe()

    assert LogFrame.objects.get() == log_frame


@pytest.mark.django_db
def test_get_logframe_returns_existing_logframe_where_one_exists():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=mock.Mock(last_viewed_logframe=None))
    overview_mixin.kwargs = {}
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_returns_first_logframe_by_default():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=mock.Mock(last_viewed_logframe=None))
    overview_mixin.kwargs = {}
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_current_logframe_slug_from_current_user():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]
    request.user.last_viewed_logframe = expected_log_frame

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_current_logframe_slug_from_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
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
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    unused_logframe, expected_log_frame = G(LogFrame, n=2)
    request.user.last_viewed_logframe = unused_logframe

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_current_logframe_set_when_not_set_on_user_but_slug_in_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame == overview_mixin.request.user.last_viewed_logframe


@pytest.mark.django_db
def test_current_logframe_set_when_different_in_session_and_slug_in_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()

    unused_logframe, expected_log_frame = G(LogFrame, n=2)
    request.user.last_viewed_logframe = unused_logframe

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame == request.user.last_viewed_logframe


@pytest.mark.django_db
def test_get_logframe_stores_logframe_id_in_request_user():
    request = RequestFactory().get('/')
    request.user = mock.Mock()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame == request.user.last_viewed_logframe


@pytest.mark.django_db
def test_get_logframe_doesnt_set_logframe_id_in_session_if_present():
    request = RequestFactory().get('/')
    request.user = mock.Mock(save=mock.Mock())

    logframe = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    request.user.last_viewed_logframe = logframe

    overview_mixin.get_logframe()

    assert not request.user.save.called


@pytest.mark.django_db
def test_update_session_logframe_updates_user_last_viewed_logframe():
    request = mock.Mock(user=mock.Mock(last_viewed_logframe=None))

    logframe = N(LogFrame, slug='test_slug')
    update_current_logframe(request.user, logframe)

    assert 'test_slug' == request.user.last_viewed_logframe.slug
