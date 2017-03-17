from django.conf.urls import url
from contacts.views import (
    AddContact, DeleteContact, ListContacts, ListContactsExport
)


urlpatterns = [
    url(r'edit/$', AddContact.as_view(), name='contact_add'),
    url(r'delete/(?P<pk>\d+)/$', DeleteContact.as_view(),
        name='contact_delete'),
    url(r'export_as_csv/$', ListContactsExport.as_view(), {'format': 'csv'},
        name='contact_list_csv'),
    url(r'export_as_excel/$', ListContactsExport.as_view(), {'format': 'excel'},
        name='contact_list_excel'),
    url(r'$', ListContacts.as_view(), name='contact_list'),
]
