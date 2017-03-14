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
    permission_required = 'organization.add_organization'


class OrganizationEdit(LoginRequiredMixin, GetOrgBySlugMixin, OrganizationUpdate):
    pass


class OrganizationDelete(LoginRequiredMixin, GetOrgBySlugMixin, BaseOrganizationDelete):
    pass
