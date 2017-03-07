from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from organizations.forms import OrganizationAddForm
from organizations.utils import create_organization

from .backends import invitation_backend


class CreateOrganizationForm(OrganizationAddForm):
    def save(self, **kwargs):
        """
        Create the organization, then get the user, then make the owner.
        """
        is_active = True
        try:
            user = get_user_model().objects.get(business_email=self.cleaned_data['email'])
        except get_user_model().DoesNotExist:
            user = invitation_backend().invite_by_email(
                    self.cleaned_data['email'],
                    **{'domain': get_current_site(self.request),
                        'organization': self.cleaned_data['name'],
                        'sender': self.request.user, 'created': True})
            is_active = False
        return create_organization(
            user, self.cleaned_data['name'],
            self.cleaned_data['slug'], is_active=is_active)
