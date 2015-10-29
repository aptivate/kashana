from django.conf.urls import url
from .views import (
    Home, DashboardView
)

urlpatterns = [
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'', Home.as_view(), name='home'),
]
