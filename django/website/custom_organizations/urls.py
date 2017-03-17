from django.conf.urls import url

from .views import OrganizationCreate, OrganizationEdit, OrganizationDelete


urlpatterns = [
    url(r'add/', OrganizationCreate.as_view(), name='organization_add'),
    url(r'(?P<org_slug>[-a-zA-Z0-9_]+)/edit/$', OrganizationEdit.as_view(), name='organization_edit'),
    url(r'(?P<org_slug>[-a-zA-Z0-9_]+)/delete/$', OrganizationDelete.as_view(), name="organization_delete"),
]
