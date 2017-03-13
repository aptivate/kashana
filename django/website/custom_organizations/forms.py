from uuslug import uuslug

from organizations.forms import OrganizationAddForm
from organizations.models import Organization
from organizations.utils import create_organization


class CreateOrganizationForm(OrganizationAddForm):
    class Meta(object):
        exclude = ('email', 'slug', 'users', 'is_active')

    def save(self, **kwargs):
        """
        Create the organization, then make the current user the owner.
        """
        return create_organization(
            self.request.user, self.cleaned_data['name'],
            uuslug(self.cleaned_data['name'], self.instance), is_active=True)
