from django.conf.urls import patterns, url
from .views import ExportLogframeData


urlpatterns = patterns('',
    url(r'^data/(?P<pk>\d+)/(?P<period>\d{4}-\d{2}-\d{2})/$',
        ExportLogframeData.as_view(),
        name="export-logframe-data-period"),
)
