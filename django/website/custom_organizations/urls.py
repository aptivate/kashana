from django.conf.urls import url
from custom_organizations.views import OrganizationCreate


urlpatterns = [
    url('create/', OrganizationCreate.as_view(), name='organization_create'),
]
