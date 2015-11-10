from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core import mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.test.client import RequestFactory

from mock import Mock, patch
import pytest

from ..forms import ContactPasswordResetForm
from ..views.activation import (
    change_password,
    ActivationEmailsView,
    ResetPassword,
    SendActivationEmailView
)

User = get_user_model()


def test_reset_password_subject_contains_site_name():
    assert '{0}: password recovery'.format(settings.SITE_NAME) == ResetPassword().get_subject()


@pytest.mark.django_db
@patch('contacts.views.activation.messages', new=Mock())
def test_reset_password_view_sends_email_when_form_valid():
    user = User.objects.create(business_email='test@example.com')
    form = ContactPasswordResetForm(data={'email': 'test@example.com'})
    form.users_cache = [user]

    request = RequestFactory().get('/')

    mail.outbox = []

    view = ResetPassword()
    view.request = request
    view.form_valid(form)

    assert len(mail.outbox) > 0


@pytest.mark.django_db
@patch('contacts.views.activation.messages', new=Mock())
def test_reset_password_view_doesnt_send_email_when_form_invalid():
    user = User.objects.create(business_email='test@example.com')
    form = ContactPasswordResetForm()
    form.users_cache = [user]

    request = RequestFactory().get('/')

    mail.outbox = []

    view = ResetPassword()
    view.request = request
    view.form_invalid(form)

    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_reset_password_view_displays_message_when_form_valid():
    user = User.objects.create(business_email='test@example.com')
    form = ContactPasswordResetForm(data={'email': 'test@example.com'})
    form.users_cache = [user]

    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)
    MessageMiddleware().process_request(request)

    view = ResetPassword()
    view.request = request
    view.form_valid(form)

    assert 'success' == request._messages._queued_messages[0].tags
    assert 'Reset password email was sent to this contact. Please check your mailbox for further instructions.' == request._messages._queued_messages[0].message


@pytest.mark.django_db
@patch('contacts.views.activation.messages', new=Mock())
def test_reset_password_view_redirects_on_success():
    user = User.objects.create(business_email='test@example.com')
    form = ContactPasswordResetForm(data={'email': 'test@example.com'})
    form.users_cache = [user]

    request = RequestFactory().get('/')

    view = ResetPassword()
    view.request = request
    response = view.form_valid(form)

    assert isinstance(response, HttpResponseRedirect)
    assert reverse('login') == response.url


@pytest.mark.django_db
def test_reset_password_view_displays_error_message_when_form_invalid():
    form = ContactPasswordResetForm()
    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)
    MessageMiddleware().process_request(request)

    view = ResetPassword()
    view.request = request
    view.form_invalid(form)

    assert 'error' == request._messages._queued_messages[0].tags
    assert 'Email could not be sent. Check if provided email is correct.' == request._messages._queued_messages[0].message


@pytest.mark.django_db
def test_password_change_view_redirects_to_personal_edit_on_success():
    user = User.objects.create(business_email='test@example.com')
    user.set_password('password')
    user.save()

    request = RequestFactory().post(
        '/',
        data={
            'old_password': 'password',
            'new_password1': 'new_pass',
            'new_password2': 'new_pass',
    })
    request.user = user
    request.csrf_processing_done = True

    response = change_password(request)

    assert isinstance(response, HttpResponseRedirect)
    assert reverse('personal_edit') == response.url


@pytest.mark.django_db
def test_email_acitvation_view_shows_error_on_invalid_form():
    user = User.objects.create(business_email='test@example.com')
    user.is_active = False
    user.save()

    request = RequestFactory().get('/')
    SessionMiddleware().process_request(request)
    MessageMiddleware().process_request(request)

    view = SendActivationEmailView()
    view.send_email(request, user.pk)

    assert 'error' == request._messages._queued_messages[0].tags
    assert 'Email could not be sent. Check if business email is correct.' == request._messages._queued_messages[0].message


def test_activation_emails_view_throws_not_implemented_error_on_get_subject():
    with pytest.raises(NotImplementedError):
        ActivationEmailsView().get_subject()
