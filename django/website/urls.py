from django.conf.urls import include, url
# from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import logframe.urls
import api.urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('contacts.auth_urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(api.urls)),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^export/', include('export.urls')),
    url(r'', include(logframe.urls)),

    # This requires that static files are served from the 'static' folder.
    # The apache conf is set up to do this for you, but you will need to do it on
    # dev
    url(r'favicon.ico', RedirectView.as_view(
        url='{0}images/favicon.ico'.format(settings.STATIC_URL))),

    # LAST - redirect from root URL to the logframe app
    # url(r'^$', RedirectView.as_view(url=reverse_lazy('logframe-overview', args=(1,)))),
    url(r'', include('dashboard.urls')),
]
