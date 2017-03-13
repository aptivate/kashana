from uuslug import uuslug

from floppyforms.__future__.models import ModelForm, ModelChoiceField
from organizations.models import Organization
from organizations.utils import create_organization


class CreateOrganizationForm(ModelForm):

    class Meta(object):
        exclude = ('slug', 'users', 'is_active')
        model = Organization

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CreateOrganizationForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        """
        Create the organization, then make the current user the owner.
        """
        return create_organization(
            self.request.user, self.cleaned_data['name'],
            uuslug(self.cleaned_data['name'], self.instance), is_active=True)
