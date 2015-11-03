import pytest

from contacts.forms import (
    AddContactForm,
    UpdatePersonalInfoForm,
    ContactPasswordResetForm
)


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
