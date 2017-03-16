from django.conf.urls import url
from .views import SendActivationEmailView, UpdateContact

urlpatterns = [
    url(r'activate/(?P<pk>\d+)/$', SendActivationEmailView.as_view(),
        name='contact_claim_account'),
    url(r'edit/(?P<pk>\d+)/$', UpdateContact.as_view(),
        name='contact_update'),
]
