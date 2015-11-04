import pytest

from mock import Mock

from ..forms import (
    AddContactForm,
    ContactPasswordResetForm,
    UpdatePersonalInfoForm,
    UpdateContactForm
)
from contacts.forms import AdminUserCreationForm, AdminUserChangeForm


def test_is_active_is_only_difference_on_add_contact_form():
    """
    Update personal info and add contact forms should be the same except
    that add contact is for administrators and should have the is_active
    field.
    """
    update_personal_info = UpdatePersonalInfoForm()
    add_contact = AddContactForm()
    assert update_personal_info._meta.widgets == add_contact._meta.widgets
    assert update_personal_info._meta.model == add_contact._meta.model

    # Subtract elements we expect to see on add_contact_form
    # to update_personal_info so we can compare
    add_contact_flds = add_contact.Meta.fieldsets[0][1]['fields']
    update_personal_flds = update_personal_info.Meta.fieldsets[0][1]['fields']
    difference = list(set(add_contact_flds) - set(update_personal_flds))
    assert difference == ['is_active']


@pytest.mark.django_db
def test_contact_password_reset_form_can_handle_invalid_user():
    form = ContactPasswordResetForm(data={'email': 'test@example.org'})
    try:
        form.is_valid()
    except AttributeError:
        assert False, "An attribute error shouldn't be raised here"


def test_update_contact_form_only_sends_email_change_notifications_when_email_changed():
    form = UpdateContactForm()
    form.notify_email_change = Mock()
    form.instance = Mock(
            has_usable_password=lambda: True,
            business_email='test1@example.org'
    )
    form.cleaned_data = {'business_email': 'test@example.com'}

    old_get_method = form._meta.model.objects.get
    form._meta.model.objects.get = lambda pk: Mock(business_email='test@example.com')

    form.send_notification_if_email_changed()

    form._meta.model.objects.get = old_get_method

    assert not form.notify_email_change.called


def test_username_not_in_admin_user_creation_form():
    form = AdminUserCreationForm()
    assert 'username' not in form.fields


def test_username_not_in_admin_user_change_form():
    form = AdminUserChangeForm()
    assert 'username' not in form.fields
