import pytest

from django.core.urlresolvers import reverse
from django.test.client import RequestFactory

from contacts.tests.factories import (
    UserFactory
)
from dashboard.views import Home


def get_response(user):
    view = Home.as_view()
    request = RequestFactory().get('/')
    request.user = user
    return view(request)


#
# Test redirects
#
@pytest.mark.django_db
def test_everyone_redirected_to_dashboard():
    user = UserFactory()
    user.is_superuser = True

    response = get_response(user)
    assert response.status_code == 302
    assert response['Location'] == reverse(u"dashboard")
