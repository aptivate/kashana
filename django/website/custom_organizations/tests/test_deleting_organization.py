from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from mock import Mock

from ..views import OrganizationDelete


def test_deleting_organization_redirects_to_dashboard():
    view = OrganizationDelete()
    assert reverse('dashboard') == view.get_success_url()


def test_deleting_last_viewed_organization_sets_it_to_none():
    org = Mock()

    request = RequestFactory().get('/')
    request.user = Mock(preferences=Mock(last_viewed_organization=org))

    view = OrganizationDelete()
    view.get_object = lambda: org
    view.request = request
    view.delete(request)

    assert request.user.preferences.last_viewed_organization is None


def test_deleting_other_organization_leaves_it_unchanged():
    org = Mock()

    request = RequestFactory().get('/')
    request.user = Mock(preferences=Mock(last_viewed_organization=org))

    view = OrganizationDelete()
    view.get_object = Mock()
    view.request = request
    view.delete(request)

    assert org == request.user.preferences.last_viewed_organization


def test_user_preferences_updated_if_last_viewed_organization_deleted():
    org = Mock()

    request = RequestFactory().get('/')
    request.user = Mock(preferences=Mock(last_viewed_organization=org, save=Mock()))

    view = OrganizationDelete()
    view.get_object = lambda: org
    view.request = request
    view.delete(request)

    assert request.user.preferences.save.called
