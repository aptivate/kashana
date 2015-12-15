from django.conf.urls import url
from django.views.generic.base import View
from .views import (
    Home, DashboardView, SwitchLogframes
)

urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'logframes/switch$', SwitchLogframes.as_view(), name='switch-logframes'),
    url(r'^dashboard/(?P<slug>[\w_-]+)', View.as_view(), name='logframe-dashboard'),
    url(r'', Home.as_view(), name='home'),
]
