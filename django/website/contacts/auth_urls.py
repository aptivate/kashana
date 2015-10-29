from django.conf.urls import patterns, url
from django.contrib.auth.views import (
    login, logout_then_login, password_reset_confirm
)
from .views import ResetPassword, change_password


urlpatterns = patterns('',
    url(r'login/$', login, name='login'),
    url(r'logout/$', logout_then_login, name='logout'),

    # Activation and password reset
    url(r'password_reset/$', ResetPassword.as_view(), name='password_reset'),
    url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, {'post_reset_redirect': '/'}, name='password_reset_confirm'),
    url(r'password_change/$', change_password, name='password_change'),
)
