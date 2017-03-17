# coding=utf-8
from __future__ import unicode_literals
import pytest

from contacts.views import UpdateContact

from .factories import UserFactory, ContactsManagerFactory
from organizations.models import Organization


@pytest.mark.integration
@pytest.mark.groupfactory
@pytest.mark.django_db
def test_activation_email_link_is_rendered_if_contact_has_not_set_password(rf):
    view = UpdateContact.as_view()
    contact_for_editing = UserFactory()
    request_user = ContactsManagerFactory()
    request_user.preferences.last_viewed_organization = Organization(slug='test')
    request = rf.get('/')
    request.user = request_user
    response = view(request, pk=contact_for_editing.id)
    response.render()
    assert 'Account not claimed' in response.content.decode('utf-8')
    # The button name that triggers an activation email to be sent is the
    # save-and-email button - see views_test
    assert 'name="save-and-email"' in response.content.decode('utf-8')


@pytest.mark.integration
@pytest.mark.groupfactory
@pytest.mark.django_db
def test_activation_email_link_is_not_rendered_if_contact_has_set_password(rf):
    view = UpdateContact.as_view()
    contact_for_editing = UserFactory()
    contact_for_editing.set_password('åρｒｏｐｅｒρäѕｓɰòｒｄ')
    contact_for_editing.save()
    request_user = ContactsManagerFactory()
    request_user.preferences.last_viewed_organization = Organization(slug='test')
    request = rf.get('/')
    request.user = request_user
    response = view(request, pk=contact_for_editing.id)
    response.render()
    assert 'Account not claimed' not in response.content.decode('utf-8')
    # The button name that triggers an activation email to be sent is the
    # save-and-email button - see views_test
    assert 'name="save-and-email"' not in response.content.decode('utf-8')
