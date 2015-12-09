from django.contrib.sessions.middleware import SessionMiddleware
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
    log_frame = overview_mixin.get_logframe()

    assert log_frame == LogFrame.objects.get()


@pytest.mark.django_db
def test_get_logframe_returns_existing_logframe_where_one_exists():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(session={})
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_returns_first_logframe_by_default():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(session={})
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_current_logframe_id_from_session():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]
    request.session['current_logframe'] = expected_log_frame.id

    overview_mixin = OverviewMixin()
    overview_mixin.request = request

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_stores_logframe_id_in_session():
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request

    overview_mixin.get_logframe()

    assert expected_log_frame.id == request.session['current_logframe']
