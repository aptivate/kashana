from django.test.client import RequestFactory

from mock import Mock

from ..views import DashboardOrganizationSelection


def test_organization_dashboard_uses_users_organization_list():
    view = DashboardOrganizationSelection()

    request = RequestFactory().get('/')
    request.user = Mock(organizations_organization=Mock(all=Mock()))

    view.request = request

    view.get_queryset()

    assert request.user.organizations_organization.all.called
