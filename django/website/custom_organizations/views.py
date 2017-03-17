from django.core.urlresolvers import reverse

from braces.views import PermissionRequiredMixin, LoginRequiredMixin
from organizations.views import (
    OrganizationCreate as BaseOrganizationCreate,
    OrganizationDelete as BaseOrganizationDelete,
    OrganizationUpdate
)

from .forms import CreateOrganizationForm
from .mixins import GetOrgBySlugMixin


class OrganizationCreate(PermissionRequiredMixin, BaseOrganizationCreate):
    form_class = CreateOrganizationForm
    permission_required = 'organizations.add_organization'

    def get_success_url(self):
        reverse('dashboard')

    def form_valid(self, form):
        response = BaseOrganizationCreate.form_valid(self, form)
        self.request.user.preferences.last_viewed_organization = self.object
        self.request.user.preferences.save()
        return response


class OrganizationEdit(LoginRequiredMixin, GetOrgBySlugMixin, OrganizationUpdate):
    pass


class OrganizationDelete(LoginRequiredMixin, GetOrgBySlugMixin, BaseOrganizationDelete):
    pass
