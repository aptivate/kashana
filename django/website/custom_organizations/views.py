from braces.views import PermissionRequiredMixin
from organizations.views import OrganizationCreate as BaseOrganizationCreate

from .forms import CreateOrganizationForm


class OrganizationCreate(PermissionRequiredMixin, BaseOrganizationCreate):
    form_class = CreateOrganizationForm
    permission_required = 'organization.add_organization'
