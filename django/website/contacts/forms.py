from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, PasswordResetForm
)
from django.forms import (
    ModelForm, ValidationError, ImageField
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _

import mail
import floppyforms as forms
from floppyforms.fields import EmailField
from form_utils.forms import BetterModelForm, BetterForm
from registration.forms import RegistrationForm as BaseRegistrationForm

from main.widgets import (
    BetterFileInput,
    BetterImageInput,
)
from .models import User

TITLES = (
    'Dr', 'Hon', 'Mrs', 'Ms', 'Mr', 'Prof', 'His Excellency',
    'Her Excellency', 'Rt.Hon', 'Assoc. Prof'
)


class TitleInput(forms.TextInput):
    def get_context_data(self):
        ctx = super(TitleInput, self).get_context_data()
        ctx.update({
            'datalist': TITLES
        })
        return ctx


#######################################################################
# Contacts forms
#######################################################################
class UpdatePersonalInfoForm(BetterModelForm):
    class Meta:
        model = User
        fields = [
            'business_email', 'first_name', 'last_name'
        ]
        fieldsets = [('all', {'fields': [
            'business_email', 'first_name',
            'last_name']})]


class AddContactForm(BetterModelForm):
    class Meta:
        model = User
        fields = [
            'business_email', 'first_name', 'last_name', 'is_active',
        ]
        fieldsets = [('all', {'fields': [
            'business_email', 'first_name', 'last_name', 'is_active', ]})]


class UpdateContactForm(AddContactForm):
    def notify_email_change(self,
                            old_address,
                            new_address,
                            subject='{0}: email change notification'.format(settings.SITE_NAME),
                            template_name='contacts/email/email_changed_body.email'):
        ctx = {
            'user': self.instance,
            'old_email': old_address,
            'new_email': new_address,
            'site_name': settings.SITE_NAME,
            'contact_address': settings.CONTACT_ADDRESS
        }
        options = {
            'subject': subject,
            'to': [old_address, new_address],
            'template_name': template_name,
            'context': ctx
        }
        mail.notify(options)

    def send_notification_if_email_changed(self):
        if self.instance and self.instance.has_usable_password():
            old = self._meta.model.objects.get(pk=self.instance.pk)
            old_email = old.business_email
            if self.cleaned_data['business_email'] != old_email:
                self.notify_email_change(
                    old_email,
                    self.cleaned_data['business_email'])

    def save(self, *args, **kwargs):
        self.send_notification_if_email_changed()
        return super(UpdateContactForm, self).save(*args, **kwargs)


class DeleteContactForm(ModelForm):

    class Meta:
        model = User
        fields = ()


#######################################################################
# Admin contacts forms
#######################################################################
class AdminUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    class Meta:
        model = User
        fields = ("business_email",)


class AdminUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = '__all__'


#######################################################################
# Password reset forms
#######################################################################
class ContactPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        error_messages={
            'unknown': _(
                "We couldn't find a user for that email address. Please "
                "check that you typed the address correctly."
            )
        }
    )

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        self.users_cache = UserModel._default_manager.filter(
            business_email__iexact=email)
        if not len(self.users_cache):
            raise ValidationError(self.fields['email'].error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise ValidationError(self.fields['email'].error_messages['unknown'])
        return email

    def save(self, subject,
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            ctx = {
                'email': user.business_email,
                'site': settings.SITE_HOSTNAME,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
                'site_name': settings.SITE_NAME,
                'contact_address': settings.CONTACT_ADDRESS,
            }
            options = {
                'subject': subject,
                'from_email': from_email,
                'to': [user.business_email],
                'template_name': email_template_name,
                'context': ctx
            }
            mail.notify(options)


# The registration process assumes a field called 'email' on the user model
# Our model uses a field called 'business_email' for this purpose, so we need
# to map the email field onto business_email
class RegistrationForm(BetterModelForm, BaseRegistrationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        self.instance.business_email = self.cleaned_data['email']
        return BaseRegistrationForm.save(self, commit=commit)
