from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django_dynamic_fixture import G, N
import pytest

from ..forms import (
    AddContactForm,
    AdminUserCreationForm,
    AdminUserChangeForm,
    ContactPasswordResetForm,
    UpdatePersonalInfoForm,
)
from .context_managers import doesnt_raise
from contacts.forms import RegistrationForm


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
    with doesnt_raise(AttributeError, "An attribute error shouldn't be raised here"):
        form.is_valid()


def test_username_not_in_admin_user_creation_form():
    form = AdminUserCreationForm()
    assert 'username' not in form.fields


def test_username_not_in_admin_user_change_form():
    form = AdminUserChangeForm()
    assert 'username' not in form.fields


@pytest.mark.django_db
def test_user_id_encoded_in_base_64_when_sending_password_reset_email():
    mail.outbox = []

    User = get_user_model()
    user = G(User)
    encoded_username = urlsafe_base64_encode(force_bytes(user.pk))

    form = ContactPasswordResetForm(data={'email': user.business_email})
    form.is_valid()
    form.save('Test Email')

    assert encoded_username in mail.outbox[0].body


@pytest.mark.django_db
def test_registration_form_sets_business_email():
    user_data = N(get_user_model(), persist_dependencies=False)
    form = RegistrationForm(data={
        'email': user_data.business_email,
        'first_name': user_data.first_name,
        'last_name': user_data.last_name,
        'password1': 'password',
        'password2': 'password'
    })
    form.is_valid()
    user = form.save()

    assert user.business_email == user_data.business_email
