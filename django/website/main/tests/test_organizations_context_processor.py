from django.test.client import RequestFactory

from django_dynamic_fixture import N
from mock import Mock
from organizations.models import Organization

from ..context_processors import organization_list


def test_logrames_context_processor_returns_list_of_logframes():
    organization_set = N(Organization, n=3, persist_dependencies=False)

    request = RequestFactory().get('/')
    request.user = Mock(organizations_organization=Mock(all=lambda: organization_set))

    assert {'organization_list': organization_set} == organization_list(request)
