from django.conf.urls import url
from .views import (
    Home, DashboardView, DashboardLogframeSelection, SwitchLogframes
)

urlpatterns = [
    url(r'^dashboard/$', DashboardLogframeSelection.as_view(), name='dashboard'),
    url(r'logframes/switch$', SwitchLogframes.as_view(), name='switch-logframes'),
    url(r'^dashboard/(?P<org_slug>[\w\d_-]+)/(?P<slug>[\w\d_-]+)/$', DashboardView.as_view(), name='logframe-dashboard'),
    url(r'', Home.as_view(), name='home'),
]
