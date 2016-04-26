from django.conf.urls import url
from contacts.views import (
    AddContact, UpdateContact, DeleteContact, ListContacts,
    SendActivationEmailView,
    UpdatePersonalInfo, ListContactsExport, SetUserPermissions
)


urlpatterns = [
    url(r'edit/$', AddContact.as_view(), name='contact_add'),
    url(r'edit/(?P<pk>\d+)/$', UpdateContact.as_view(),
        name='contact_update'),
    url(r'edit/(?P<pk>\d+)/permissions/$', SetUserPermissions.as_view(),
        name='contact_permissions_update'),
    url(r'delete/(?P<pk>\d+)/$', DeleteContact.as_view(),
        name='contact_delete'),
    url(r'activate/(?P<pk>\d+)/$', SendActivationEmailView.as_view(),
        name='contact_claim_account'),
    url(r'personal/$', UpdatePersonalInfo.as_view(), name='personal_edit'),
    url(r'export_as_csv/$', ListContactsExport.as_view(), {'format': 'csv'},
        name='contact_list_csv'),
    url(r'export_as_excel/$', ListContactsExport.as_view(), {'format': 'excel'},
        name='contact_list_excel'),
    url(r'$', ListContacts.as_view(), name='contact_list'),
]
