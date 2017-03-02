from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

from django_dynamic_fixture import G, N
import mock
from organizations.models import Organization
import pytest

from logframe.models import LogFrame

from ..mixins import OverviewMixin, update_last_viewed_item


User = get_user_model()


class MockUser(object):
    preferences = None
    organizations_organization = mock.Mock(first=lambda: None)

    def __init__(self):
        self.preferences = mock.Mock(last_viewed_logframe=None, last_viewed_organization=None)

    def save(self):
        pass


@pytest.mark.django_db
def test_get_logframe_returns_new_logframe_if_none_exists():
    LogFrame.objects.all().delete()

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=MockUser())
    overview_mixin.request.user.preferences.last_viewed_organization = G(Organization)
    overview_mixin.kwargs = {}

    log_frame = overview_mixin.get_logframe()

    assert LogFrame.objects.get() == log_frame


@pytest.mark.django_db
def test_get_logframe_returns_existing_logframe_where_one_exists():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=MockUser())
    overview_mixin.request.user.preferences.last_viewed_organization = expected_log_frame.organization
    overview_mixin.kwargs = {}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_returns_first_logframe_by_default():
    LogFrame.objects.all().delete()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=MockUser())
    overview_mixin.request.user.preferences.last_viewed_organization = expected_log_frame.organization
    overview_mixin.kwargs = {}
    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_last_viewed_logframe_slug_from_current_user():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]
    request.user.preferences.last_viewed_logframe = expected_log_frame
    request.user.preferences.last_viewed_organization = expected_log_frame.organization

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_get_logframe_gets_last_viewed_logframe_slug_from_kwargs():
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
def test_get_logframe_gets_last_viewed_logframe_slug_from_kwargs_in_preference_to_session():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    unused_logframe, expected_log_frame = G(LogFrame, n=2)
    request.user.preferences.last_viewed_logframe = unused_logframe

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    actual_log_frame = overview_mixin.get_logframe()

    assert expected_log_frame == actual_log_frame


@pytest.mark.django_db
def test_last_viewed_logframe_set_when_not_set_on_user_but_slug_in_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    expected_log_frame = G(LogFrame, n=2)[1]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame == overview_mixin.request.user.preferences.last_viewed_logframe


@pytest.mark.django_db
def test_last_viewed_logframe_set_when_different_in_session_and_slug_in_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()

    unused_logframe, expected_log_frame = G(LogFrame, n=2)
    request.user.preferences.last_viewed_logframe = unused_logframe

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame == request.user.preferences.last_viewed_logframe


@pytest.mark.django_db
def test_get_logframe_stores_logframe_id_in_request_user():
    request = RequestFactory().get('/')
    request.user = mock.Mock()

    expected_log_frame = G(LogFrame, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'slug': expected_log_frame.slug}

    overview_mixin.get_logframe()

    assert expected_log_frame == request.user.preferences.last_viewed_logframe


@pytest.mark.django_db
def test_get_logframe_doesnt_set_logframe_id_in_session_if_present():
    request = RequestFactory().get('/')
    request.user = mock.Mock(save=mock.Mock())

    logframe = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    request.user.preferences.last_viewed_logframe = logframe

    overview_mixin.get_logframe()

    assert not request.user.save.called


@pytest.mark.django_db
def test_update_session_logframe_updates_user_last_viewed_logframe():
    request = mock.Mock(user=MockUser())

    logframe = N(LogFrame, slug='test_slug')
    update_last_viewed_item(request.user, logframe)

    assert 'test_slug' == request.user.preferences.last_viewed_logframe.slug


@pytest.mark.django_db
def test_get_organization_returns_new_organization_if_none_exists():
    Organization.objects.all().delete()

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=G(User))
    overview_mixin.kwargs = {}

    organization = overview_mixin.get_organization()

    assert Organization.objects.get() == organization


@pytest.mark.django_db
def test_get_organization_returns_existing_organization_where_one_exists():
    Organization.objects.all().delete()

    expected_organization = G(Organization)

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=MockUser())
    overview_mixin.request.user.organizations_organization = Organization.objects.all()
    overview_mixin.kwargs = {}

    actual_organization = overview_mixin.get_organization()

    assert expected_organization == actual_organization


@pytest.mark.django_db
def test_get_organization_returns_first_organization_by_default():
    Organization.objects.all().delete()

    expected_organization = G(Organization, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = mock.Mock(user=MockUser())
    overview_mixin.request.user.organizations_organization = Organization.objects.all()
    overview_mixin.kwargs = {}
    actual_organization = overview_mixin.get_organization()

    assert expected_organization == actual_organization


@pytest.mark.django_db
def test_organization_gets_last_viewed_organization_slug_from_current_user():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    expected_organization = G(Organization, n=2)[1]
    request.user.preferences.last_viewed_organization = expected_organization

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    actual_organization = overview_mixin.get_organization()

    assert expected_organization == actual_organization


@pytest.mark.django_db
def test_get_organization_gets_last_viewed_organization_slug_from_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock(organizations_organization=mock.Mock())
    SessionMiddleware().process_request(request)

    expected_organization = G(Organization, n=2)[1]
    request.user.organizations_organization.first = lambda: expected_organization
    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'org_slug': expected_organization.slug}

    actual_organization = overview_mixin.get_organization()

    assert expected_organization == actual_organization


@pytest.mark.django_db
def test_get_organization_gets_last_viewed_organization_slug_from_kwargs_in_preference_to_session():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    unused_organization, expected_organization = G(Organization, n=2)
    request.user.preferences.last_viewed_organization = unused_organization

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'org_slug': expected_organization.slug}

    actual_organization = overview_mixin.get_organization()

    assert expected_organization == actual_organization


@pytest.mark.django_db
def test_last_viewed_organization_set_when_not_set_on_user_but_slug_in_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()
    SessionMiddleware().process_request(request)

    expected_organization = G(Organization, n=2)[1]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'org_slug': expected_organization.slug}

    overview_mixin.get_organization()

    assert expected_organization == overview_mixin.request.user.preferences.last_viewed_organization


@pytest.mark.django_db
def test_last_viewed_organization_set_when_different_in_session_and_slug_in_kwargs():
    request = RequestFactory().get('/')
    request.user = mock.Mock()

    unused_organization, expected_organization = G(Organization, n=2)
    request.user.preferences.last_viewed_organization = unused_organization

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'org_slug': expected_organization.slug}

    overview_mixin.get_organization()

    assert expected_organization == request.user.preferences.last_viewed_organization


@pytest.mark.django_db
def test_get_organization_stores_organization_id_in_request_user():
    request = RequestFactory().get('/')
    request.user = mock.Mock()

    expected_organization = G(Organization, n=2)[0]

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {'org_slug': expected_organization.slug}

    overview_mixin.get_organization()

    assert expected_organization == request.user.preferences.last_viewed_organization


@pytest.mark.django_db
def test_get_organization_doesnt_set_organization_id_in_session_if_present():
    request = RequestFactory().get('/')
    request.user = mock.Mock(save=mock.Mock())

    organization = G(LogFrame)

    overview_mixin = OverviewMixin()
    overview_mixin.request = request
    overview_mixin.kwargs = {}

    request.user.preferences.last_viewed_organization = organization

    overview_mixin.get_organization()

    assert not request.user.save.called


@pytest.mark.django_db
def test_update_session_organization_updates_user_last_viewed_organization():
    request = mock.Mock(user=MockUser())

    organization = N(Organization, slug='test_slug')
    update_last_viewed_item(request.user, organization)

    assert 'test_slug' == request.user.preferences.last_viewed_organization.slug
