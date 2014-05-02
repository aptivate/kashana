from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, RedirectView

from contacts.models import User
from contacts.forms import ContactPasswordResetForm


########################################################################
# Account activation and password reset
########################################################################
class ResetPassword(FormView):
    from_address = settings.EMAIL_BOT_ADDRESS
    email_template = 'contacts/email/password_reset_request.email'
    template_name = 'registration/password_reset.html'
    form_class = ContactPasswordResetForm

    def get_subject(self):
        return "{0}: password recovery".format(settings.SITE_NAME)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'from_email': self.from_address,
            'email_template_name': self.email_template,
            'subject': self.get_subject(),
            'request': self.request,
        }
        form.save(**opts)
        messages.success(
            self.request, ('Reset password email was sent to this '
                           'contact. Please check your mailbox for further '
                           'instructions.'))
        return HttpResponseRedirect(reverse('login'))

    def form_invalid(self, form):
        messages.error(self.request, ('Email could not be sent. Check if '
                                      'provided email is correct.'))
        return self.render_to_response(self.get_context_data(form=form))


def change_password(request):
    return password_change(request,
                           post_change_redirect=reverse('personal_edit'))


class ActivationEmailsView(RedirectView):
    from_address = settings.EMAIL_BOT_ADDRESS
    email_template = 'contacts/email/activation_body.email'

    def get_subject(self):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        self.send_emails(request, **kwargs)
        return super(ActivationEmailsView, self).get(request, *args, **kwargs)


class SendActivationEmailView(ActivationEmailsView):
    def get_redirect_url(self, **kwargs):
        return reverse("contact_update", args=[self.pk])

    def get_subject(self):
        return "Please activate your {0} account".format(settings.SITE_NAME)

    def send_email(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        form = ContactPasswordResetForm({'email': obj.business_email})
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'from_email': self.from_address,
                'email_template_name': self.email_template,
                'subject': self.get_subject(),
                'request': request,
            }
            form.save(**opts)
            messages.success(request,
                             'Activation email was sent to this contact.')
        else:
            messages.error(request,
                           'Email could not be sent. \
                                   Check if business email is correct.')

    def send_emails(self, request, **kwargs):
        self.pk = int(kwargs['pk'])
        self.send_email(request, self.pk)
