from django.test.client import RequestFactory

import mock
from mock import patch

from ..views import OrganizationCreate


@patch('custom_organizations.views.BaseOrganizationCreate', new=mock.Mock())
def test_new_organization_set_as_last_viewed():
    view = OrganizationCreate()
    view.object = mock.Mock()

    request = RequestFactory()
    request.user = mock.Mock(preferences=mock.Mock())

    view.request = request

    view.form_valid(mock.Mock())
    assert view.object == request.user.preferences.last_viewed_organization


@patch('custom_organizations.views.BaseOrganizationCreate', new=mock.Mock())
def test_prefrences_updated():
    view = OrganizationCreate()
    view.object = mock.Mock()

    request = RequestFactory()
    request.user = mock.Mock(preferences=mock.Mock())

    view.request = request

    view.form_valid(mock.Mock())
    assert request.user.preferences.save.called
