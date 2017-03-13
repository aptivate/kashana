from django.conf.urls import url
from custom_organizations.views import OrganizationCreate


urlpatterns = [
    url('add/', OrganizationCreate.as_view(), name='organization_add'),
]
