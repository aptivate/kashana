from django.conf.urls import patterns, url
from .views import (
    Home, DashboardView
)

urlpatterns = patterns(
    '',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'', Home.as_view(), name='home'),
)
